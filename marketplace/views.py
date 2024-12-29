from django.shortcuts import render
from vendor.models import Vendor
from django.shortcuts import get_object_or_404
from menu.models import Category,FoodItem
from django.db.models import Prefetch
from django.http import HttpResponse,JsonResponse
from .models import Cart
from marketplace.context_processors import get_cart_counter,get_cart_amount

# Create your views here.
def marketplace(request):
    vendors=Vendor.objects.filter(is_approved=True,user__is_active=True)
    vendor_count=vendors.count()
    context={
        'vendors':vendors,
        'vendor_count':vendor_count,
    }
    return render(request, 'marketplace/listing.html',context)

def vendor_detail(request,vendor_slug):
    vendor=get_object_or_404(Vendor,vendor_slug=vendor_slug)
    Categories=Category.objects.filter(vendor=vendor).prefetch_related(
        Prefetch('fooditems', queryset=FoodItem.objects.filter(is_available=True)),
    )
    if request.user.is_authenticated:
        cart_items=Cart.objects.filter(user=request.user)
    else:
        cart_items=None
    context={
        'vendor':vendor,
        'categories':Categories,
        'cart_items': cart_items,
    }
    return render(request,'marketplace/vendor_detail.html',context)

def add_to_cart(request,food_id):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with')=='XMLHttpRequest':
            #Check if fooditem exists
            try:
                fooditem=FoodItem.objects.get(id=food_id)
                try:
                    chkcart=Cart.objects.get(user=request.user,fooditem=fooditem)
                    chkcart.quantity+=1
                    chkcart.save()
                    return JsonResponse({'status':'Success','message':'This food is added succesfully','cart_counter':get_cart_counter(request),'qty':chkcart.quantity,'cart_amount':get_cart_amount(request)})
                except:
                    chkcart=Cart.objects.create(user=request.user,fooditem=fooditem,quantity=1,)
                    return JsonResponse({'status':'success','message':'New food is added','cart_counter':get_cart_counter(request),'qty':chkcart.quantity,'cart_amount':get_cart_amount(request)})
            except:
                return JsonResponse({'status':'Failed','message':'Invalid request !'},status=400)
        else:
            return JsonResponse({'status':'Failed','message':'Invalid Request'})
    else:
        return JsonResponse({'status':'login_required','message':'Please login to continue'})
    

def decrease_cart(request,food_id):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with')=='XMLHttpRequest':
            #Check if fooditem exists
            try:
                fooditem=FoodItem.objects.get(id=food_id)
                # decrease the quantity if >=1
                try:
                    chkcart=Cart.objects.get(user=request.user,fooditem=fooditem)
                    if chkcart.quantity>=1:
                      chkcart.quantity =chkcart.quantity-1
                      chkcart.save()
                      return JsonResponse({'status':'Success','message':'This food is removed succesfully','cart_counter':get_cart_counter(request),'qty':chkcart.quantity,'cart_amount':get_cart_amount(request)})
                    else:
                        chkcart.delete()
                        chkcart.quantity=0
                        return JsonResponse({'status':'Failed','message':'No food available to remove','cart_counter':get_cart_counter(request),'qty':chkcart.quantity})
                except:
                    chkcart=Cart.objects.create(user=request.user,fooditem=fooditem,quantity=1)
                    return JsonResponse({'status':'Failed','message':'You did not have this food in the cart !'})
            except:
                return JsonResponse({'status':'Failed','message':'Invalid request !'},status=400)
        else:
            return JsonResponse({'status':'Failed','message':'Invalid Request'})
    else:
        return JsonResponse({'status':'login_required','message':'Please login to continue'})
    
def cart(request):
    cart_items=Cart.objects.filter(user=request.user).order_by('created_at')
    context={
        'cart_items':cart_items,
    }
    return render(request,'marketplace/cart.html',context)

def delete_cart(request,cart_id):
    if request.user.is_authenticated:
       if request.headers.get('x-requested-with')=='XMLHttpRequest':
           try:
               cart_item=Cart.objects.get(user=request.user,id=cart_id)
               if cart_item:
                   cart_item.delete()
                   return JsonResponse({'status':'Success','message':'Cart item has been deleted succesfully','cart_counter':get_cart_counter(request),'cart_amount':get_cart_amount(request)}) 
           except:
               return JsonResponse({'status':'Failed','message':'Cart item does not exist..!'})
       else:
           return JsonResponse({'status':'Failed','message':'Invalid Request'})
       
           

    
    