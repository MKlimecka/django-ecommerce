from django.urls import path 
from django.urls.conf import include
from django.shortcuts import render
from rest_framework_nested import routers
from django.views.generic import TemplateView
import store.views as views




router = routers.DefaultRouter()
router.register('products', views.ProductViewSet, basename='products')
router.register('collections', views.CollectionViewSet)
router.register('carts', views.CartViewSet, basename='cart')
router.register('cart/items', views.CartItemViewSet, basename='cart-items')
router.register('customers', views.CustomerViewSet)
router.register('orders', views.OrderViewSet, basename='orders')
router.register('favorites', views.FavoriteViewSet, basename='favorites')


products_router = routers.NestedDefaultRouter(router, 'products', lookup='product')
products_router.register('reviews', views.ReviewViewSet, basename='product-reviews')
products_router.register('images', views.ProductImageViewSet, basename= 'product-images')


carts_router = routers.NestedDefaultRouter(router,'carts', lookup='cart')
carts_router.register('items', views.CartItemViewSet, basename='cart-items')

urlpatterns = router.urls + products_router.urls + carts_router.urls + [
    path('product_list/', views.product_list_view, name='product_list'),
    path('', TemplateView.as_view(template_name='index.html')),
    path('api_list/', views.api_list_view, name='api_list'),
    path('login/', views.login_view, name='login'),
    path('favorites/', views.favorites_view, name='favorites'),
    path('account/', views.account_view, name='account'),
    path('register/', views.register_view, name='register'),
    path('cart/', views.cart_view, name='cart'),
]



