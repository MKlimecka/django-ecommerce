from uuid import UUID
from amqp import NotFound
from django.forms import ValidationError
from django.shortcuts import get_object_or_404, render
from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, DestroyModelMixin, UpdateModelMixin
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.permissions import IsAuthenticated ,AllowAny, IsAdminUser, DjangoModelPermissions, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework import status
from .pagination import DefaultPagination
from .models  import Product, Collection, Review, Cart, Cart_item, Customer, Order, ProductImage, Order_item, \
Favorite
from .filters import ProductFilter
from .permissions import IsAdminOrReadOnly, ViewCustomerHistoryPermission
from .serializers import ProductSerializer, CollectionSerializer, ReviewSerializer, CartSerializer, \
    CartItemSerializer, AddCartItemSerializer, UpdateCartItemSerializer, CustomerSerializer, OrderSerializer, \
     CreateOrderSerializer, UpdateOrderSerializer, ProductImageSerializer, FavoriteSerializer


class ProductViewSet(ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.prefetch_related('images').all()
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ProductFilter
    pagination_class = DefaultPagination
    permission_classes = [IsAdminOrReadOnly]
    search_fields = ['title', 'description']
    ordering_fields = ['unit_price', 'last_update']

    def get_serializer_context(self):
        return {'request': self.request}
    
    def destroy(self, request, *args, **kwargs):
         if Order_item.objects.filter(product_id=kwargs['pk']).count() > 0 :
            return Response({'error': 'Product cannot be deleted.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
         return super().destroy(request, *args, **kwargs)


class CollectionViewSet(ModelViewSet):

    queryset = Collection.objects.annotate(
            products_count=Count('products')).all()
    serializer_class = CollectionSerializer
    permission_classes = [IsAdminOrReadOnly]

    def destroy(self, request, *args, **kwargs):
        if Collection.products.count() > 0:
            return Response({'error': 'Collection cannot be deleted.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)
    
class ReviewViewSet(ModelViewSet):

    serializer_class = ReviewSerializer

    def get_queryset(self):
        return Review.objects.filter(product_id=self.kwargs['product_pk'])
    
    def get_serializer_context(self):
        return {'product_id': self.kwargs['product_pk']}
    

class CartViewSet(CreateModelMixin, 
                  RetrieveModelMixin, 
                  DestroyModelMixin, 
                  GenericViewSet):
    
    http_method_names =['get', 'post', 'patch', 'delete']
     
    #  queryset = Cart.objects.prefetch_related('items__products').all()
    
    serializer_class = CartSerializer
    permission_classes = [AllowAny]


    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return Cart.objects\
            .filter(user=user)\
            .prefetch_related('items__product')
        return Cart.objects.none()

     
    def perform_create(self, serializer):
        user = None
        if self.request.user.is_authenticated:
            serializer.save(user=user)
        
    @action(detail=False, methods=['get'], url_path='me', permission_classes=[AllowAny])
    def get_my_cart(self, request):
        user = request.user
        if user.is_authenticated:
            cart = Cart.objects.filter(user=user).first()
        else:
            cart = None
        if cart:
            serializer = self.get_serializer(cart)
            return Response(serializer.data)
        return Response({'detail': 'Cart not found'}, status=404)


class CartItemViewSet(ModelViewSet):
    http_method_names =['get', 'post', 'patch', 'delete']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddCartItemSerializer
        elif self.request.method == 'PATCH':
            return UpdateCartItemSerializer
        return CartItemSerializer
    
    def get_serializer_context(self):
        try:
            cart = Cart.objects.get(user=self.request.user)
        except Cart.DoesNotExist:
            raise NotFound('Cart not found.')
        return {'cart_id': str(cart.id)}

    def get_queryset(self):
        try:
            cart = Cart.objects.get(user=self.request.user)
        except Cart.DoesNotExist:
            raise NotFound('No cart found for this user')
        return Cart_item.objects\
            .filter(cart=cart)\
            .select_related('product')



class CustomerViewSet(ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAdminUser]

    @action(detail=True, permission_classes=[ViewCustomerHistoryPermission])
    def history(self, request, pk):
        return Response('ok')

    @action(detail=False, methods=['GET','PUT'], permission_classes=[IsAuthenticated])
    def me(self, request):

        customer = Customer.objects.get(user_id=request.user.id)
        if request.method == 'GET':
            customer = Customer.objects.get(user_id=request.user.id)
            serializer = CustomerSerializer(customer)
            return Response(serializer.data)
        elif request.method == 'PUT':
            serializer = CustomerSerializer(customer, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)


class OrderViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']

    def get_permissions(self):
        if self.request.method in ['PATCH', 'DELETE']:
            return [IsAdminUser()]
        return [IsAuthenticated()]
        

    def create(self, request, *args, **kwargs):
        serializer = CreateOrderSerializer(
            data=request.data,
            context={'user_id': self.request.user.id})
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        serializer = OrderSerializer(order)
        return Response(serializer.data)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateOrderSerializer
        elif self.request.method == 'PATCH':
            return UpdateOrderSerializer
        return OrderSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Order.objects.all()
        
        customer_id = Customer.objects.only('id').get(user_id=user.id)
        return Order.objects.filter(customer_id=customer_id)

class ProductImageViewSet(ModelViewSet):
    serializer_class = ProductImageSerializer

    def get_serializer_context(self):
        return {'product_id': self.kwargs['product_pk']}
    
    def get_queryset(self):
        return ProductImage.objects.filter(product_id=self.kwargs['product_pk'])
    
class FavoriteViewSet(ModelViewSet):
    serializer_class = FavoriteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        try:
            customer = Customer.objects.get(user_id=self.request.user)
            return Favorite.objects.filter(customer=customer)
        except Customer.DoesNotExist:
            return Favorite.objects.none()

    def perform_create(self, serializer):
        try:
            customer = Customer.objects.get(user_id=self.request.user)
            serializer.save(customer=customer)
        except Customer.DoesNotExist:
            raise ValidationError ('No customer account')

    @action(detail=False, methods=['POST'], url_path='toggle')   
    def toggle(self, request):
        customer = Customer.objects.get(user_id=self.request.user)
        product_id = request.data.get('product')
        favorite, created = Favorite.objects.get_or_create(
            customer=customer,
            product_id=product_id 
        )
        if not created:
            favorite.delete()
            return Response('Removed from favorites')
        return Response('Added to favorites')
    
    @action(detail=False, methods=['get'], url_path='me', permission_classes=[IsAuthenticated])
    def get_my_favorites(self, request):
        customer = get_object_or_404(Customer, user=request.user)
        favorites = Favorite.objects.filter(customer=customer).select_related('product')
        products = [f.product for f in favorites]
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    
def product_list_view(request):
        products = Product.objects.all()
        return render(request, 'store/product_list.html', {'products':products})

def api_list_view(request):
    endpoints = [
        {'name': 'Products', 'url': '/store/products/', 'description': 'Returns a list od avaliable products'},
        {'name': 'Collections', 'url': '/store/collections/', 'description': 'Returns product collections'},
        {'name': 'Customer', 'url': '/store/auth/users/me/', 'description': "Returns the current customer", 'auth': True},
        {'name': 'Cart', 'url': '/store/carts/me/', 'description': "Returns the current customer's cart", 'auth': True},
        {'name': 'Cart/items', 'url': '/store/cart/items/', 'description': 'Allows adding to cart', 'auth': True},
        {'name': 'Orders', 'url': '/store/orders/', 'description': "Returns the current customer's order history", 'auth': True},
        {'name': 'Favorites', 'url': '/store/favorites/me/', 'description': "Returns the current customer's favorite items", 'auth': True},
    ]
    return render(request, 'store/api_list.html', {'endpoints':endpoints})

def login_view(request):
    return render(request, 'store/login.html')

def favorites_view(request):
    return render(request, 'store/favorites.html')

def account_view(request):
    return render(request, 'store/account.html')

def register_view(request):
    return render(request, 'store/register.html')

def cart_view(request):
    return render(request, 'store/cart.html')








