from django.shortcuts import render
from accounts.models import UserProfile
from vendor.models import Vendor
from django.shortcuts import get_object_or_404
from menu.models import Category, FoodItem
from django.db.models import Prefetch, Avg
from django.http import HttpResponse, JsonResponse
from .models import Cart, Review, Coupon, Favourite
from marketplace.context_processors import get_cart_counter, get_cart_amount
from django.db.models import Q
from vendor.models import OpeningHour
from datetime import date, datetime
from orders.forms import OrderForm
from django.shortcuts import redirect

# Create your views here.
def marketplace(request):
    vendors=Vendor.objects.filter(is_approved=True,user__is_active=True)
    vendor_count=vendors.count()
    context={
        'vendors':vendors,
        'vendor_count':vendor_count,
    }
    return render(request, 'marketplace/listing.html',context)

def vendor_detail(request, vendor_slug):
    vendor = get_object_or_404(Vendor, vendor_slug=vendor_slug)

    categories = Category.objects.filter(vendor=vendor).prefetch_related(
        Prefetch('fooditems', queryset=FoodItem.objects.filter(is_available=True)),
    )

    opening_hours = OpeningHour.objects.filter(vendor=vendor).order_by('day', '-from_hour')
    today_date = date.today()
    today = today_date.isoweekday()
    current_opening_hour = OpeningHour.objects.filter(vendor=vendor, day=today)

    now = datetime.now().time()
    is_open = False
    for hour in current_opening_hour:
        start = datetime.strptime(hour.from_hour, "%I:%M %p").time()
        end = datetime.strptime(hour.to_hour, "%I:%M %p").time()
        if start <= now <= end:
            is_open = True
            break

    cart_items = Cart.objects.filter(user=request.user) if request.user.is_authenticated else None

    reviews = Review.objects.filter(vendor=vendor).order_by('-created_at')
    avg_rating = reviews.aggregate(avg=Avg('rating'))['avg'] or 0
    user_review = None
    is_favourite = False
    if request.user.is_authenticated:
        user_review = Review.objects.filter(user=request.user, vendor=vendor).first()
        is_favourite = Favourite.objects.filter(user=request.user, vendor=vendor).exists()

    context = {
        'vendor': vendor,
        'categories': categories,
        'cart_items': cart_items,
        'opening_hours': opening_hours,
        'current_opening_hours': current_opening_hour,
        'is_open': is_open,
        'reviews': reviews,
        'avg_rating': round(avg_rating, 1),
        'review_count': reviews.count(),
        'user_review': user_review,
        'is_favourite': is_favourite,
    }

    return render(request, 'marketplace/vendor_detail.html', context)
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

def search(request):
    keyword = request.GET.get('keyword', '').strip()  # Extract the 'keyword' parameter from the request
    vendors = Vendor.objects.none()  # Start with an empty queryset

    if keyword:  # Only perform the search if a keyword is provided
        # Get vendors based on matching food items
        food_item_vendors = FoodItem.objects.filter(
            food_title__icontains=keyword, is_available=True
        ).values_list('vendor', flat=True)

        # Get vendors based on matching vendor names
        vendors = Vendor.objects.filter(
            Q(id__in=food_item_vendors) |  # Vendors with matching food items
            Q(vendor_name__icontains=keyword, is_approved=True, user__is_active=True)  # Vendors with matching names
        )

    vendor_count = vendors.count()  # Count the results

    context = {
        'vendors': vendors,  # Filtered vendors
        'vendor_count': vendor_count,  # Count of results
    }
    return render(request, 'marketplace/listing.html', context)


def checkout(request):
    cart_items=Cart.objects.filter(user=request.user).order_by('created_at')
    cart_count=cart_items.count()
    user_profile=UserProfile.objects.get(user=request.user)
    saved_addresses = request.user.addresses.all()
    default_values = {
        'first_name': request.user.first_name,
        'last_name': request.user.last_name,
        'phone': request.user.phone,
        'email': request.user.email,
        'address': user_profile.address,
        'country': user_profile.country,
        'state': user_profile.state,
        'city': user_profile.city,
        'pin_code': user_profile.pincode,
    }
    form=OrderForm(initial=default_values)
    if cart_count<=0:
        return redirect('marketplace')
    # Pass coupon discount if one is in session
    coupon_discount = request.session.get('coupon_discount', 0)
    coupon_code = request.session.get('coupon_code', '')
    context={
        'form': form,
        'cart_items': cart_items,
        'saved_addresses': saved_addresses,
        'coupon_discount': coupon_discount,
        'applied_coupon': coupon_code,
    }
    return render(request,'marketplace/checkout.html',context)


def submit_review(request, vendor_id):
    if not request.user.is_authenticated:
        return JsonResponse({'status': 'login_required', 'message': 'Please login to leave a review.'})
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        vendor = get_object_or_404(Vendor, id=vendor_id)
        rating = request.POST.get('rating')
        comment = request.POST.get('comment', '').strip()
        if not rating or not rating.isdigit() or int(rating) not in range(1, 6):
            return JsonResponse({'status': 'error', 'message': 'Please select a valid rating (1-5).'})
        _, created = Review.objects.update_or_create(
            user=request.user,
            vendor=vendor,
            defaults={'rating': int(rating), 'comment': comment},
        )
        avg = Review.objects.filter(vendor=vendor).aggregate(avg=Avg('rating'))['avg'] or 0
        return JsonResponse({
            'status': 'success',
            'message': 'Review submitted!' if created else 'Review updated!',
            'username': request.user.get_full_name() or request.user.email,
            'rating': rating,
            'comment': comment,
            'avg_rating': round(avg, 1),
        })
    return JsonResponse({'status': 'error', 'message': 'Invalid request.'})


def apply_coupon(request):
    if not request.user.is_authenticated:
        return JsonResponse({'status': 'login_required', 'message': 'Please login.'})
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        code = request.POST.get('coupon_code', '').strip().upper()
        cart_amount = get_cart_amount(request)
        grand_total = cart_amount['grand_total']
        try:
            coupon = Coupon.objects.get(code=code)
            is_valid, message = coupon.is_valid(grand_total)
            if is_valid:
                discount = coupon.get_discount_amount(grand_total)
                final_total = round(float(grand_total) - discount, 2)
                request.session['coupon_code'] = code
                request.session['coupon_discount'] = discount
                return JsonResponse({
                    'status': 'success',
                    'message': f'Coupon applied! You saved ${discount:.2f}.',
                    'discount': discount,
                    'final_total': final_total,
                })
            return JsonResponse({'status': 'error', 'message': message})
        except Coupon.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Invalid coupon code.'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request.'})


def remove_coupon(request):
    request.session.pop('coupon_code', None)
    request.session.pop('coupon_discount', None)
    cart_amount = get_cart_amount(request)
    return JsonResponse({'status': 'success', 'grand_total': float(cart_amount['grand_total'])})


def toggle_favourite(request, vendor_id):
    if not request.user.is_authenticated:
        return JsonResponse({'status': 'login_required', 'message': 'Please login to save favourites.'})
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        vendor = get_object_or_404(Vendor, id=vendor_id)
        fav = Favourite.objects.filter(user=request.user, vendor=vendor)
        if fav.exists():
            fav.delete()
            return JsonResponse({'status': 'removed', 'message': 'Removed from favourites.'})
        Favourite.objects.create(user=request.user, vendor=vendor)
        return JsonResponse({'status': 'added', 'message': 'Added to favourites!'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request.'})

       
           

    
    