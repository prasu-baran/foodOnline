from .models import Cart
from menu.models import FoodItem

def get_cart_counter(request):
    cart_count = 0  # Initialize cart_count outside the if statement
    
    if request.user.is_authenticated:
        try:
            cart_items = Cart.objects.filter(user=request.user)
            if cart_items:
                for cart_item in cart_items:
                    cart_count += cart_item.quantity
        except:
            cart_count = 0
    
    # Return dictionary outside all conditions
    return {'cart_count': cart_count}

def get_cart_amount(request):
    subtotal=0
    tax=0
    grand_total=0
    if request.user.is_authenticated:
        cart_items=Cart.objects.filter(user=request.user)
        for item in cart_items:
            fooditem=FoodItem.objects.get(pk=item.fooditem.id)
            subtotal+=fooditem.price*item.quantity
            
        grand_total=subtotal+tax
    print(subtotal)
    print(grand_total)
    return dict(subtotal=subtotal,tax=tax,grand_total=grand_total)