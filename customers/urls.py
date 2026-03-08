from django.urls import path
from accounts import views as AccountViews
from . import views

urlpatterns = [
    path('', AccountViews.custdashboard, name='customer'),
    path('profile/', views.cprofile, name='cprofile'),
    path('my_orders/', views.my_orders, name='customer_my_orders'),
    path('order_detail/<int:order_number>/', views.order_detail, name='order_detail'),

    # Reorder
    path('reorder/<int:order_number>/', views.reorder, name='reorder'),

    # Favourites
    path('my_favourites/', views.my_favourites, name='my_favourites'),

    # Addresses
    path('my_addresses/', views.my_addresses, name='my_addresses'),
    path('add_address/', views.add_address, name='add_address'),
    path('delete_address/<int:address_id>/', views.delete_address, name='delete_address'),
    path('set_default_address/<int:address_id>/', views.set_default_address, name='set_default_address'),
]
