from django.db import models
from accounts.models import User
from menu.models import FoodItem
from vendor.models import Vendor
# Create your models here.
class Cart(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    fooditem=models.ForeignKey(FoodItem,on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        return self.user
    
class Tax(models.Model):
    tax_type=models.CharField(max_length=20,unique=True)
    tax_percentage=models.DecimalField(decimal_places=2,max_digits=4,verbose_name='Tax Percentage (%)')
    is_active=models.BooleanField(default=True)
    
    class Meta:
        verbose_name_plural='tax'

    def __self__(self):
        return self.tax_type


class Review(models.Model):
    RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='reviews')
    order = models.ForeignKey('orders.Order', on_delete=models.SET_NULL, null=True, blank=True)
    rating = models.PositiveSmallIntegerField(choices=RATING_CHOICES)
    comment = models.TextField(max_length=500, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'vendor')

    def __str__(self):
        return f'{self.user.email} - {self.vendor.vendor_name} ({self.rating}★)'


class Coupon(models.Model):
    DISCOUNT_TYPE = (
        ('percentage', 'Percentage'),
        ('flat', 'Flat Amount'),
    )
    code = models.CharField(max_length=20, unique=True)
    discount_type = models.CharField(max_length=10, choices=DISCOUNT_TYPE, default='flat')
    discount_value = models.DecimalField(max_digits=6, decimal_places=2)
    min_order_amount = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    max_uses = models.PositiveIntegerField(default=0, help_text="0 = unlimited")
    used_count = models.PositiveIntegerField(default=0)
    expiry_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.code

    def is_valid(self, order_amount):
        from django.utils import timezone
        if not self.is_active:
            return False, "Coupon is not active."
        if self.expiry_date and self.expiry_date < timezone.now().date():
            return False, "Coupon has expired."
        if self.max_uses > 0 and self.used_count >= self.max_uses:
            return False, "Coupon usage limit reached."
        if float(order_amount) < float(self.min_order_amount):
            return False, f"Minimum order amount is ${self.min_order_amount}."
        return True, "Valid"

    def get_discount_amount(self, order_amount):
        if self.discount_type == 'percentage':
            return round((float(self.discount_value) / 100) * float(order_amount), 2)
        return round(float(min(self.discount_value, order_amount)), 2)


class Favourite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='favourited_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'vendor')

    def __str__(self):
        return f'{self.user.email} likes {self.vendor.vendor_name}'