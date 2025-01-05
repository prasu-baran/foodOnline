from django.contrib import admin
from .models import Order,OrderedFood,Payment

class OrderedFoodInline(admin.TabularInline):
    model = OrderedFood
    readonly_fields = ('order', 'payment', 'user', 'fooditem', 'quantity', 'price', 'amount')
    extra = 0
    
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'name', 'phone', 'email', 'total', 'payment_method', 'status', 'order_placed_to', 'is_ordered']
    inlines = [OrderedFoodInline]


# Register your models here.
admin.site.register(Order)
admin.site.register(OrderedFood)
admin.site.register(Payment)