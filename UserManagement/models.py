from django.db import models
from OrganisationManager.models import cmpny_mastr,brnch_mstr
# Create your models here.
from django.contrib.auth.models import AbstractUser,AbstractBaseUser,BaseUserManager

from phonenumber_field.modelfields import PhoneNumberField
from .manager import CustomUserManager
from django.contrib.auth.models import User,Group

class CustomUser(AbstractUser):
    email = models.EmailField(("email address"), unique=True)
    company_role = models.CharField(max_length=100,blank=True)
    contact_number = models.CharField(max_length=20)  # Added max_length for ContactNumber field
    # created_by = models.ForeignKey('self', on_delete=models.CASCADE, null=True,blank=True, related_name='added_users')
    companies = models.ManyToManyField('OrganisationManager.cmpny_mastr', blank=True,null=True)
    branches = models.ManyToManyField('OrganisationManager.brnch_mstr', blank=True,null=True)
    is_ess = models.BooleanField(default=False,null=True,blank =True)
    USERNAME_FIELD = 'username'  # Change USERNAME_FIELD to 'username'
    REQUIRED_FIELDS = ['email']  # Remove 'username' from REQUIRED_FIELDS

    objects = CustomUserManager()

    def save_is_ess(self, *args, **kwargs):
        emp_master_instance = getattr(self, 'emp_created_by1', None)

        if emp_master_instance:
            # Update the is_ess field based on emp_master
            self.is_ess = emp_master_instance.is_ess

        super().save(*args, **kwargs)






    def save(self, *args, **kwargs):
        # Set is_active to True before saving
        self.is_active = True
        super().save(*args, **kwargs)
    
    
    
class CustomUserGroup(models.Model):
    name = models.CharField(max_length=50, unique=True)
    user = models.ManyToManyField(CustomUser,limit_choices_to = {'is_ess': False})
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    # Add any additional fields if neede