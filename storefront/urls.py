"""
URL configuration for storefront project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from store import views as store_views
# from debug_toolbar.toolbar import debug_toolbar_urls

admin.site.site_header = 'Storefront Admin'
admin.site.index_title = 'Admin'


urlpatterns = [

    path('', include('core.urls')),
    path('admin/', admin.site.urls),
    path('playground/', include('playground.urls')),
    path('store/', include('store.urls')),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('api_list/', store_views.api_list_view, name='api_list'),
    path('product_list/', store_views.product_list_view, name='product_list'),
    path('login/', store_views.login_view, name='login'),
    path('register/', store_views.register_view, name='register'),
    path('account/', store_views.account_view, name='account'),
    path('favorites/', store_views.favorites_view, name='favorites'),
    path('cart/', store_views.cart_view, name='cart'),
    path('', TemplateView.as_view(template_name='store/index.html'))

]
if settings.DEBUG:
    import debug_toolbar
    urlpatterns +=[
        path('__debug__/', include(debug_toolbar.urls)),
    ]
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    # urlpatterns += [path('silk/', include('silk.urls', namespace='silk'))]

