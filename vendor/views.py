from django.shortcuts import render,get_object_or_404,redirect

from orders.models import Order, OrderedFood
from .forms import VendorForm,OpeningHourForm
from accounts.forms import UserProfileForm
from accounts.models import UserProfile
from .models import Vendor,OpeningHour,DAYS
from django.contrib import messages
from django.contrib.auth.decorators import login_required,user_passes_test
from accounts.views import check_role_vendor
from menu.models import Category
from menu.models import FoodItem
from menu.forms import CategoryForm,FoodItemForm
from django.template.defaultfilters import slugify
from django.http import HttpResponse
from django.db import IntegrityError
from django.http import JsonResponse


def get_vendor(request):
    vendor=Vendor.objects.get(user=request.user)
    return vendor
# Create your views here.
@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def vprofile(request):
    
    profile =get_object_or_404(UserProfile,user=request.user)
    vendor =get_object_or_404(Vendor,user=request.user)
    
    if request.method =='POST':
        profile_form = UserProfileForm(request.POST,request.FILES,instance=profile)
        vendor_form = VendorForm(request.POST,request.FILES,instance=vendor)
        if profile_form.is_valid() and vendor_form.is_valid():
            profile_form.save()
            vendor_form.save()
            messages.success(request,'Settings updated.')
            return redirect('vprofile')
        else:
            print(profile_form.errors)
            print(vendor_form.errors)
    else:
        profile_form=UserProfileForm(instance= profile)
        vendor_form=VendorForm(instance=vendor)
    
    context={
        'profile_form':profile_form,
        'vendor_form':vendor_form,
        'profile':profile,
        'vendor':vendor,
    }
    return render(request, 'vendor/vprofile.html',context)


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def menu_builder(request):
    vendor=get_vendor(request)
    categories=Category.objects.filter(vendor=vendor)
    context= {
        'categories':categories,
        
    }
    return render(request,'vendor/menu_builder.html',context)


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def fooditems_by_category(request,pk=None):
    vendor=get_vendor(request)
    category=get_object_or_404(Category,pk=pk)
    fooditems=FoodItem.objects.filter(vendor=vendor,category=category)
    context={
        'fooditems':fooditems,
        'category':category,
        
    }
    return render(request,'vendor/fooditems_by_category.html',context)

def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category_name = form.cleaned_data['category_name']
            category = form.save(commit=False)
            category.vendor = get_vendor(request)
            category.slug = slugify(category_name)
            print('fsfsfsfsfsfssfsssf')
            print(category.category_name)
            
            category.save()
            messages.success(request, 'Category added successfully!')
            return redirect('menu_builder')
        else:
            print(form.errors)

    else:
        form = CategoryForm()
    context = {
        'form': form,
    }
    return render(request, 'vendor/add_category.html', context)

def edit_category(request,pk=None):
    category=get_object_or_404(Category,pk=pk)
    if request.method=='POST':
        form=CategoryForm(request.POST,instance=category)
        if form.is_valid():
            category_name=form.cleaned_data['category_name']
            category=form.save(commit=False)
            category.vendor=get_vendor(request)
            category.slug=slugify(category_name)
            form.save()
            messages.success(request,'Category added succesfully!')
            return redirect('menu_builder')
    else:   
         form=CategoryForm(instance=category)
    context= {
        'form':form,
        'category':category,
    }
    return render(request,'vendor/edit_category.html',context)

def delete_category(request,pk=None):
    category=get_object_or_404(Category,pk=pk)
    category.delete()
    messages.success(request,'Category has been deleted successfully!')
    return redirect('menu_builder')

def add_food(request):
    if request.method == 'POST':
        form = FoodItemForm(request.POST, request.FILES)
        if form.is_valid():
            foodtitle = form.cleaned_data['food_title']
            food = form.save(commit=False)
            food.vendor = get_vendor(request)
            food.slug = slugify(foodtitle)
            form.save()
            messages.success(request, 'Food Item added successfully!')
            return redirect('fooditems_by_category', food.category.id)
        else:
            # Handle invalid form by rendering the form again with error messages
            context = {
                'form': form,
            }
            return render(request, 'vendor/add_food.html', context)  # Return an HttpResponse
    else:
        form = FoodItemForm()
        form.fields['category'].queryset=Category.objects.filter(vendor=get_vendor(request))
        context = {
            'form': form,
        }
        return render(request, 'vendor/add_food.html', context)

def edit_food(request,pk=None):
    food=get_object_or_404(FoodItem,pk=pk)
    if request.method=='POST':
        form=FoodItemForm(request.POST,request.FILES,instance=food)
        if form.is_valid():
            foodtitle=form.cleaned_data['food_title']
            food=form.save(commit=False)
            food.vendor=get_vendor(request)
            food.slug=slugify(foodtitle)
            form.save()
            messages.success(request,'Food added succesfully!')
            return redirect('menu_builder')
        else:
            print(form.errors)
    else:   
         form=FoodItemForm(instance=food)
         form.fields['category'].queryset=Category.objects.filter(vendor=get_vendor(request))
    context= {
        'form':form,
        'food':food,
    }
    return render(request,'vendor/edit_food.html',context)

def delete_food(request,pk=None):
    food=get_object_or_404(FoodItem,pk=pk)
    food.delete()
    messages.success(request,'Food item has been deleted succesfully !')
    return redirect('fooditem_by_category',food.category.id)
    
    
def opening_hours(request):
    opening_hours=OpeningHour.objects.filter(vendor=get_vendor(request))
    form=OpeningHourForm()
    context={
        'form':form,
        'opening_hours':opening_hours
    }
    return render(request,'vendor/opening_hours.html',context)

def add_opening_hour(request):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.method == 'POST':
            day = request.POST.get('day')
            from_hour = request.POST.get('from_hour')
            to_hour = request.POST.get('to_hour')
            is_closed = request.POST.get('is_closed')

            # Validate inputs
            if not all([day, from_hour, to_hour, is_closed]):
                return JsonResponse({'status': 'failed', 'error': 'Missing required fields'})

            try:
                opening_hour = OpeningHour.objects.create(
                    vendor=get_vendor(request),
                    day=day,
                    from_hour=from_hour,
                    to_hour=to_hour,
                    is_closed=is_closed == 'True'
                )
                
                # Get the day name from DAYS tuple
                day_name = dict(DAYS).get(int(day), 'Unknown Day')
                
                response = {
                    'status': 'success',
                    'id': opening_hour.id,
                    'day': day_name,  # Send the day name instead of number
                    'from_hour': opening_hour.from_hour,
                    'to_hour': opening_hour.to_hour,
                    'is_closed': opening_hour.is_closed
                }
                return JsonResponse(response)
            except IntegrityError as e:
                response = {'status': 'failed', 'error': str(e)}
                return JsonResponse(response)
        else:
            return HttpResponse('Invalid request', status=400)
    else:
        return HttpResponse('Unauthorized', status=401)
    
def remove_opening_hour(request, pk=None):
    if not request.user.is_authenticated:
        return JsonResponse({'status': 'error', 'message': 'Login required'}, status=401)
        
    if not request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)
        
    try:
        hour = get_object_or_404(OpeningHour, pk=pk)
        # Add permission check if needed
        # if hour.vendor != request.user.vendor:
        #     return JsonResponse({'status': 'error', 'message': 'Permission denied'}, status=403)
        hour.delete()
        return JsonResponse({'status': 'success', 'id': pk})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    
    
def order_detail(request,order_number):
    try:
        order = Order.objects.get(order_number=order_number, is_ordered=True)
        ordered_food = OrderedFood.objects.filter(order=order, fooditem__vendor=get_vendor(request))
        print(ordered_food)
        context = {
            'order': order,
            'ordered_food': ordered_food,
            'subtotal':order.get_total_by_vendor()['subtotal'],
            'tax_data':order.get_total_by_vendor()['tax_dict'],
        }
    except:
        print('sdsfsssssds')
        return redirect('vendor')
    return render(request, 'vendor/order_detail.html', context)


def vendor_my_orders(request):
    vendor = Vendor.objects.get(user=request.user)
    orders = Order.objects.filter(vendors__in=[vendor.id], is_ordered=True).order_by('created_at')
    context={
        'orders':orders,
    }
    return render(request,'vendor/my_order.html',context)
  
     