from django.urls import path
from . import views

urlpatterns = [
    path('', views.marketplace, name='marketplace'),
    path('<slug:vendor_slug>/', views.vendor_detail, name='vendor_detail'),

    # Cart
    path('add_to_cart/<int:food_id>', views.add_to_cart, name='add_to_cart'),
    path('decrease_cart/<int:food_id>', views.decrease_cart, name='decrease_cart'),
    path('delete_cart/<int:cart_id>/', views.delete_cart, name='delete_cart'),

    # Reviews
    path('submit_review/<int:vendor_id>/', views.submit_review, name='submit_review'),

    # Coupons
    path('apply_coupon/', views.apply_coupon, name='apply_coupon'),
    path('remove_coupon/', views.remove_coupon, name='remove_coupon'),

    # Favourites
    path('toggle_favourite/<int:vendor_id>/', views.toggle_favourite, name='toggle_favourite'),
]
