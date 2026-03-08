import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db.models.fields.related import OneToOneField


def generate_referral_code():
    code = str(uuid.uuid4())[:8].upper()
    return code

# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, first_name,last_name,username,email,password=None):
        if not email:
            raise ValueError('Users must have an email address')
        if not username:
            raise ValueError('Users must have a username')
        user=self.model(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,first_name,last_name,username,email,password=None):
        user=self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )
        user.is_admin= True
        user.is_active= True
        user.is_staff= True
        user.is_superadmin= True
        user.save(using=self._db)
        return user
        
class User(AbstractBaseUser):
    VENDOR=1
    CUSTOMER=2
    
    ROLE_CHOICE=(
        (VENDOR,'Restaurant'),
        (CUSTOMER,'Customer'),
    )
    first_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)
    username=models.CharField(max_length=50,unique=True)
    email=models.EmailField(max_length=100,unique=True)
    phone=models.CharField(max_length=12,blank=True)
    role=models.PositiveSmallIntegerField(choices=ROLE_CHOICE,blank=True,null=True)
    
    # required fields
    date_joined=models.DateTimeField(auto_now_add=True)
    last_login=models.DateTimeField(auto_now_add=True)
    created_date=models.DateTimeField(auto_now_add=True)
    modified_date=models.DateTimeField(auto_now_add=True)
    is_admin=models.BooleanField(default=False)
    is_staff=models.BooleanField(default=True)
    is_active=models.BooleanField(default=False)
    is_superadmin=models.BooleanField(default=False)
    referral_code=models.CharField(max_length=20, unique=True, blank=True)

    USERNAME_FIELD='email'
    REQUIRED_FIELDS=['username','first_name','last_name']
    
    objects = UserManager()
    
    def __str__(self):
        return self.email
    def has_perm(self, perm, obj=None):
        return self.is_admin
    def has_module_perms(self, app_label):
        return True
    def get_role(self):
        if self.role==self.VENDOR:
            user_role='Restaurant'
        else:
            user_role='Customer'
        return user_role

    def save(self, *args, **kwargs):
        if not self.referral_code:
            self.referral_code = generate_referral_code()
            while User.objects.filter(referral_code=self.referral_code).exists():
                self.referral_code = generate_referral_code()
        super().save(*args, **kwargs)



class UserProfile(models.Model):
    user =OneToOneField(User,on_delete=models.CASCADE,blank=True,null=True)
    profile_picture=models.ImageField(upload_to='users/profile_pictures',blank=True,null=True)
    cover_picture=models.ImageField(upload_to='users/cover_photos',blank=True,null=True)
    address=models.CharField(max_length=250,blank=True,null=True)
    country=models.CharField(max_length=15,blank=True,null=True)
    state=models.CharField(max_length=15,blank=True,null=True)
    city=models.CharField(max_length=15,blank=True,null=True)
    pincode=models.CharField(max_length=6,blank=True,null=True)
    latitude=models.CharField(max_length=20,blank=True,null=True)
    longitude=models.CharField(max_length=20,blank=True,null=True)
    loyalty_points=models.PositiveIntegerField(default=0)
    created_at=models.DateTimeField(auto_now_add=True)
    modified_at=models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.user.email

  #  def full_address(self):
       # return f"{self.address_line_1} , {self.address_line_2}"


class UserAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses')
    label = models.CharField(max_length=30, default='Home')
    address = models.CharField(max_length=250)
    country = models.CharField(max_length=30, blank=True)
    state = models.CharField(max_length=30, blank=True)
    city = models.CharField(max_length=50, blank=True)
    pincode = models.CharField(max_length=10, blank=True)
    is_default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'User Addresses'

    def save(self, *args, **kwargs):
        if self.is_default:
            UserAddress.objects.filter(user=self.user, is_default=True).exclude(pk=self.pk).update(is_default=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.user.email} - {self.label}'
