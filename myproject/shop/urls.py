from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import cart_view, update_cart, remove_cart

urlpatterns = [
    path('', views.home, name='home'),  # Home page
    path('shop/', views.shop, name='shop'),  # Shop page
    path('product/<int:id>/', views.product_detail, name='product_detail'),
    path("cart/update/<int:product_id>/", update_cart, name="update_cart"),
    path("cart/remove/<int:product_id>/", remove_cart, name="remove_cart"),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/honey/', views.add_honey_to_cart, name='add_honey_to_cart'),
    path('cart/milk/', views.add_milk_to_cart, name='add_milk_to_cart'),
    path('cart/shampoo/', views.add_shampoo_to_cart, name='add_shampoo_to_cart'),
    path('cart/', views.cart_page, name='cart'),
    path('cart/', views.cart_view, name='cart'), 
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)