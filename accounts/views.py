from django.shortcuts import render,redirect
from django.shortcuts import HttpResponse
from .forms import UserForm
from .models import User
from django.contrib import messages

# Create your views here.
def registerUser(request):
    if request.method == 'POST':
        
        form = UserForm(request.POST)
        if form.is_valid():
           #   user= form.save(commit=False)
           #  user.role= User.CUSTOMER
           # form.save()
           first_name= form.cleaned_data['first_name']
           last_name= form.cleaned_data['last_name']
           username =form.cleaned_data['username']
           email=form.cleaned_data['email']
           password =form.cleaned_data['password']
           user =User.objects.create_user(first_name=first_name,last_name=last_name,username=username,email=email,password=password)
           user.role=User.CUSTOMER
           user.save()
           messages.success(request,'Your account has been registered succesfully')
           return redirect(registerUser)
        else:
            print('Invalide form')
            print(form.errors)
            return render(request, 'accounts/registerUser.html', {'form': form})
    else:
        form = UserForm()
        context ={
            'form':form,
        }
    form =UserForm()
    context = {
        'form':form,
    }
    return render(request,'accounts/registerUser.html',context)