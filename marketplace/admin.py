from django.contrib import admin
from marketplace.models import Cart, Tax, Review, Coupon, Favourite

class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'fooditem', 'quantity', 'updated_at')

class TaxAdmin(admin.ModelAdmin):
    list_display = ('tax_type', 'tax_percentage', 'is_active')

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'vendor', 'rating', 'created_at')
    list_filter = ('rating',)

class CouponAdmin(admin.ModelAdmin):
    list_display = ('code', 'discount_type', 'discount_value', 'min_order_amount', 'used_count', 'max_uses', 'expiry_date', 'is_active')
    list_filter = ('discount_type', 'is_active')

class FavouriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'vendor', 'created_at')

admin.site.register(Cart, CartAdmin)
admin.site.register(Tax, TaxAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Coupon, CouponAdmin)
admin.site.register(Favourite, FavouriteAdmin)