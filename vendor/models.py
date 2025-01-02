from django.db import models
from accounts.models import User,UserProfile
from accounts.utils import  send_notification
from datetime import time
from datetime import date,datetime

# Create your models here.
class Vendor(models.Model):
    user=models.OneToOneField(User,related_name='user',on_delete=models.CASCADE)
    user_profile=models.OneToOneField(UserProfile,related_name='userprofile',on_delete=models.CASCADE)
    vendor_name=models.CharField(max_length=50)
    vendor_slug=models.SlugField(max_length=100,unique=True)
    vendor_license=models.ImageField(upload_to='vendor/license')
    is_approved=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    modified_at=models.DateTimeField(auto_now=True)
    
    def __str__(self):
      return self.vendor_name  
    
    def is_open(self):
      today_date = date.today()
      today = today_date.isoweekday()
        # Fetch all opening hours for the vendor
      current_opening_hours = OpeningHour.objects.filter(vendor=self,day=today)
      now = datetime.now().time() 
      is_open = False  # Initialize
      for hour in current_opening_hours:
        start = datetime.strptime(hour.from_hour, "%I:%M %p").time()
        end = datetime.strptime(hour.to_hour, "%I:%M %p").time()
        if start <= now <= end:
            is_open = True
            break
          
        return is_open
    
    
    def save(self,*args,**kwargs):
      if self.pk is not None:
        #update
        orig=Vendor.objects.get(pk=self.pk)
        if orig.is_approved != self.is_approved:
          if self.is_approved==True:
            #send notification
            mail_subject='Congratulations! Your restaurant has been approved'
            mail_template='accounts/emails/admin_approval_email.html'
            context={
              'user':self.user,
              'is_approved':self.is_approved,
            }
            send_notification(mail_subject,mail_template,context)
          else:
            #send email
            send_notification(mail_subject,mail_template,context)
            mail_subject='We are sorry to say that your food will not be published on our marketplace'
            mail_template='accounts/emails/admin_approval_email.html'
            context={
              'user':self.user,
              'is_approved':self.is_approved,
            }
      return super(Vendor,self).save(*args,**kwargs)
    
from django.db import models
from datetime import time

DAYS = [
    (1, 'Monday'),
    (2, 'Tuesday'),
    (3, 'Wednesday'),
    (4, 'Thursday'),
    (5, 'Friday'),
    (6, 'Saturday'),
    (7, 'Sunday'),
]

HOUR_OF_DAY_24 = [
    (time(h, m).strftime('%I:%M %p'), time(h, m).strftime('%I:%M %p')) 
    for h in range(24) for m in (0, 30)
]

class OpeningHour(models.Model):
    vendor = models.ForeignKey('Vendor', on_delete=models.CASCADE)
    day = models.IntegerField(choices=DAYS)
    from_hour = models.CharField(choices=HOUR_OF_DAY_24, max_length=10, blank=True)
    to_hour = models.CharField(choices=HOUR_OF_DAY_24, max_length=10, blank=True)
    is_closed = models.BooleanField(default=False)

    class Meta:
        ordering = ('day', '-from_hour')
        constraints = [
            models.UniqueConstraint(fields=['day', 'from_hour', 'to_hour','vendor'], name='unique_day_hour_range')
        ]

    def __str__(self):
        return f"{dict(DAYS).get(self.day, 'Unknown Day')}"

  