import json
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from accounts.forms import UserProfileForm, UserInfoForm
from accounts.models import UserProfile, UserAddress
from django.contrib import messages
from marketplace.models import Cart, Favourite
from orders.models import Order, OrderedFood
from marketplace.models import Review
from vendor.models import Vendor


# Create your views here.
def cprofile(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)
        user_form = UserInfoForm(request.POST, instance=request.user)
        if profile_form.is_valid() and user_form.is_valid():
            profile_form.save()
            user_form.save()
            messages.success(request, 'Profile updated')
            return redirect('cprofile')
        else:
            print(profile_form.errors)
            print(user_form.errors)
    else:
        profile_form = UserProfileForm(instance=profile)
        user_form = UserInfoForm(instance=request.user)
    context = {
        'profile_form': profile_form,
        'user_form': user_form,
        'profile': profile,
    }
    return render(request, 'customers/cprofile.html', context)


def my_orders(request):
    orders = Order.objects.filter(user=request.user, is_ordered=True).order_by('-created_at')
    context = {
        'orders': orders,
    }
    return render(request, 'customers/my_orders.html', context)


def order_detail(request, order_number):
    try:
        order = Order.objects.get(order_number=order_number, is_ordered=True)
        ordered_food = OrderedFood.objects.filter(order=order)
        subtotal = 0
        for item in ordered_food:
            subtotal += (item.price * item.quantity)
        tax_data = json.loads(order.tax_data)

        # Check if this order's vendor has already been reviewed by this user
        reviewed_vendors = {}
        if request.user.is_authenticated:
            for item in ordered_food:
                vendor = item.fooditem.vendor
                if vendor.id not in reviewed_vendors:
                    existing_review = Review.objects.filter(user=request.user, vendor=vendor).first()
                    reviewed_vendors[vendor.id] = {
                        'vendor': vendor,
                        'existing_review': existing_review,
                    }

        context = {
            'order': order,
            'ordered_food': ordered_food,
            'subtotal': subtotal,
            'tax_data': tax_data,
            'reviewed_vendors': reviewed_vendors.values(),
        }
        return render(request, 'customers/order_detail.html', context)
    except Exception:
        return redirect('customer')


@login_required(login_url='login')
def reorder(request, order_number):
    order = get_object_or_404(Order, order_number=order_number, user=request.user, is_ordered=True)
    ordered_food = OrderedFood.objects.filter(order=order)
    added = 0
    for item in ordered_food:
        if item.fooditem.is_available:
            cart_item, created = Cart.objects.get_or_create(
                user=request.user,
                fooditem=item.fooditem,
                defaults={'quantity': item.quantity},
            )
            if not created:
                cart_item.quantity += item.quantity
                cart_item.save()
            added += 1
    if added:
        messages.success(request, f'{added} item(s) added to cart from your previous order.')
    else:
        messages.warning(request, 'No available items could be added to cart.')
    return redirect('cart')


@login_required(login_url='login')
def my_favourites(request):
    favourites = Favourite.objects.filter(user=request.user).select_related(
        'vendor', 'vendor__user_profile'
    )
    context = {'favourites': favourites}
    return render(request, 'customers/my_favourites.html', context)


@login_required(login_url='login')
def my_addresses(request):
    addresses = UserAddress.objects.filter(user=request.user).order_by('-is_default', '-created_at')
    context = {'addresses': addresses}
    return render(request, 'customers/my_addresses.html', context)


@login_required(login_url='login')
def add_address(request):
    if request.method == 'POST':
        label = request.POST.get('label', 'Home').strip()
        address = request.POST.get('address', '').strip()
        country = request.POST.get('country', '').strip()
        state = request.POST.get('state', '').strip()
        city = request.POST.get('city', '').strip()
        pincode = request.POST.get('pincode', '').strip()
        is_default = request.POST.get('is_default') == 'on'
        if address:
            UserAddress.objects.create(
                user=request.user,
                label=label,
                address=address,
                country=country,
                state=state,
                city=city,
                pincode=pincode,
                is_default=is_default,
            )
            messages.success(request, 'Address added successfully.')
        else:
            messages.error(request, 'Address cannot be empty.')
    return redirect('my_addresses')


@login_required(login_url='login')
def delete_address(request, address_id):
    addr = get_object_or_404(UserAddress, id=address_id, user=request.user)
    addr.delete()
    messages.success(request, 'Address deleted.')
    return redirect('my_addresses')


@login_required(login_url='login')
def set_default_address(request, address_id):
    addr = get_object_or_404(UserAddress, id=address_id, user=request.user)
    addr.is_default = True
    addr.save()
    messages.success(request, f'"{addr.label}" set as your default address.')
    return redirect('my_addresses')
