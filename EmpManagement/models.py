
from django.contrib.contenttypes.models import ContentType
from django.db import models
import random
from django.dispatch import receiver
from django.db.models.signals import post_save,pre_save
from UserManagement.models import CustomUser
from phonenumber_field.modelfields import PhoneNumberField
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from import_export import resources, fields
from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from django import forms
import datetime,json
from django.core.validators import validate_email
from datetime import datetime
import re


class emp_master(models.Model):

    GENDER = {
        "M": "Male",
        "F": "Female",
        "O": "Other",
    }
    MARITAL_STATUS = {
        "M":"Married",
        "S":"Single",
        "D":"Other",
    }
    emp_code = models.CharField(max_length=50,unique=True,null=True,blank =True)
    emp_first_name = models.CharField(max_length=50,null=True,blank =True)
    emp_last_name = models.CharField(max_length=50,null=True,blank =True)
    emp_gender = models.CharField(max_length=10,choices=GENDER,null=True,blank =True)
    emp_date_of_birth = models.DateField(null=True,blank =True)
    emp_personal_email =  models.EmailField(unique=True,null=True,blank =True)
    is_ess=models.BooleanField(default=True,null=True,blank =True)
    emp_mobile_number_1 = models.CharField(unique=True,null=True,blank =True)
    emp_mobile_number_2 = models.CharField(null=True,blank =True)
    emp_country_id = models.ForeignKey("Core.cntry_mstr",on_delete = models.CASCADE,null=True,blank =True)
    emp_state_id = models.ForeignKey("Core.state_mstr",on_delete=models.CASCADE,null=True,blank =True)
    emp_city = models.CharField(max_length=50,null=True,blank =True)
    emp_permenent_address = models.CharField(max_length=200,null=True,blank =True)
    emp_present_address = models.CharField(max_length=200,blank=True,null=True)
    emp_status =  models.BooleanField(default=True,null=True,blank =True)
    # emp_boss = models.ForeignKey('emp_master',on_delete = models.CASCADE)
    emp_hired_date = models.DateField(null=True,blank =True)
    emp_active_date = models.DateField(null=True,blank=True)
    emp_relegion = models.CharField(max_length=50,null=True,blank =True)
    emp_profile_pic = models.ImageField(null=True,blank =True )
    emp_blood_group = models.CharField(max_length=50,blank=True)
    emp_nationality_id = models.ForeignKey("Core.Nationality",on_delete = models.CASCADE,null=True,blank =True)
    emp_marital_status = models.CharField(max_length=10,choices=MARITAL_STATUS,null=True,blank =True)
    emp_father_name = models.CharField(max_length=50,null=True,blank =True)
    emp_mother_name = models.CharField(max_length=50,null=True,blank =True)
    emp_posting_location = models.CharField(max_length=50,null=True,blank =True)
    created_at = models.DateTimeField(auto_now_add=True,null=True,blank =True)
    created_by = models.ForeignKey('UserManagement.CustomUser', on_delete=models.CASCADE, null=True,  related_name='emp_created_by1')
    updated_at = models.DateTimeField(auto_now=True,null=True,blank =True)
    updated_by = models.ForeignKey('UserManagement.CustomUser', on_delete=models.CASCADE, null=True, related_name='emp_updated_by1')
    is_active = models.BooleanField(default=True,null=True,blank =True)
    epm_ot_applicable = models.BooleanField(default=False,null=True,blank =True)
    #foreign keys 
    # emp_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    emp_company_id = models.ForeignKey("OrganisationManager.cmpny_mastr",on_delete = models.CASCADE,null=True,blank =True)
    emp_branch_id = models.ForeignKey("OrganisationManager.brnch_mstr",on_delete = models.CASCADE,null=True,blank =True)
    emp_dept_id = models.ForeignKey("OrganisationManager.dept_master",on_delete = models.CASCADE,null=True,blank =True)
    emp_desgntn_id = models.ForeignKey("OrganisationManager.desgntn_master",on_delete = models.CASCADE,null=True,blank =True)
    emp_ctgry_id = models.ForeignKey("OrganisationManager.ctgry_master",on_delete = models.CASCADE,null=True,blank =True)
    emp_languages = models.ManyToManyField("OrganisationManager.LanguageMaster",null=True,blank =True)
    
    
    def save(self, *args, **kwargs):
        if self.is_ess:

            created = not self.pk  # Check if the instance is being created for the first time
            super().save(*args, **kwargs)

            if created:
                # Create a new user with default password
                user_model = get_user_model()
                username = self.emp_code
                password = 'admin'  # You can set a default password here
                email = self.emp_personal_email
                # Create the user
                user = user_model.objects.create_user(username=username, email=email, password=password)

                # Link the user to the employee
                self.created_by = user
                user.is_ess = self.is_ess
                user.save()
                
                # Set is_ess to True
                # user.is_ess = True
                # user.save()
                # self.save()
                # super().save(*args, **kwargs)
        else:

            super().save(*args, **kwargs)

    def __str__(self):
        return self.emp_code or "Unnamed Employee"

class Emp_CustomField(models.Model):
    FIELD_TYPES = (   
        ('dropdown', 'DropdownField'),
        ('radio', 'RadioButtonField'),
       )
    emp_master = models.ForeignKey(emp_master, on_delete=models.CASCADE,related_name='custom_fields')
    field_name = models.CharField(max_length=100)  # Field name provided by end user
    field_value = models.TextField(null=True, blank=True)  # Field value provided by end user
    data_type = models.CharField(max_length=20, choices=FIELD_TYPES,null=True,blank =True)
    dropdown_values = models.JSONField(null=True, blank=True)
    radio_values = models.JSONField(null=True, blank=True)
    
    
    def save(self, *args, **kwargs):
        if self.data_type == 'dropdown':
            # Check if dropdown options are provided and valid JSON
            if self.dropdown_values:
                options = self.dropdown_values  # No need for json.loads() here

                # Assign dropdown options to the field_value if it's empty
                if not self.field_value:
                    self.field_value = json.dumps(options)
                else:
                    # If field_value is not empty, check if it's in the dropdown options
                    if self.field_value not in options.values():
                        raise ValueError("Selected value is not in the dropdown options.")

        elif self.data_type == 'radio':
            # If radio options are not provided, use an empty list
            if self.radio_values:
                options = self.radio_values  # No need for json.loads() here

                # Assign radio options to the field_value if it's empty
                if not self.field_value:
                    self.field_value = json.dumps(options)
                else:
                    # If field_value is not empty, check if it's in the radio options
                    if self.field_value not in options.values():
                        raise ValueError("Selected value is not in the radio options.")
        else:
            if isinstance(self.field_value, int) or self.field_value.isdigit():
                self.data_type = 'integer'
            elif isinstance(self.field_value, str):
                if re.match(r'\d{1,2}-\d{1,2}-\d{4}', self.field_value):
                    parts = self.field_value.split('-')
                    # Add leading zeros if necessary
                    day = parts[0].zfill(2)
                    month = parts[1].zfill(2)
                    formatted_date = f"{day}-{month}-{parts[2]}"
                    try:
                        parsed_date = datetime.strptime(formatted_date, '%d-%m-%Y').date()
                    except ValueError:
                        raise ValidationError({'field_value': ['Invalid date format. Date should be in DD-MM-YYYY format.']})
                    self.data_type = 'date'
                    self.date_field = parsed_date
                elif self.field_value.lower() in ['yes', 'no', 'true', 'false', '0', '1']:
                    self.data_type = 'boolean'
                elif re.match(r"[^@]+@[^@]+\.[^@]+", self.field_value):
                    self.data_type = 'email'
                elif self.data_type == 'dropdown':
                    # Parse dropdown options if provided
                    if self.field_value:
                        self.field_value = self.field_value.split(',')
                elif self.data_type == 'radio':
                    # Parse radio options if provided
                    if self.field_value:
                        self.field_value = self.field_value.split(',')
                else:
                    self.data_type = 'text'
            else:
                raise ValueError(f"Invalid value '{self.field_value}' for data type '{self.data_type}'.")
        
        super().save(*args, **kwargs)
    


#EMPLOYEE FAMILY(ef) data
class emp_family(models.Model):
    emp_id =models.ForeignKey('emp_master',on_delete = models.CASCADE,null=True,blank=True, related_name='emp_family')
    ef_sl_no = models.CharField(max_length=50, unique=True,null=False,blank =True,default=None)
    ef_member_name = models.CharField(max_length=50)
    emp_relation = models.CharField(max_length=50)
    ef_company_expence = models.FloatField()
    ef_date_of_birth = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('UserManagement.CustomUser', on_delete=models.SET_NULL, null=True, related_name='%(class)s_created_by')
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey('UserManagement.CustomUser', on_delete=models.SET_NULL, null=True, related_name='%(class)s_updated_by')
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        # If emp_id is not set and if this instance has an emp_id related object, set it automatically
        if not self.emp_id_id and hasattr(self, 'emp_id'):
            self.emp_id_id = self.emp_id.id
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.ef_sl_no }"
        # - {self.emp_login_id}"


class EmpFamily_CustomField(models.Model):
    FIELD_TYPES = (
        ('dropdown', 'DropdownField'),
        ('radio', 'RadioButtonField'),)
    emp_family = models.ForeignKey('emp_family', on_delete=models.CASCADE, related_name='fam_custom_fields')
    field_name = models.CharField(max_length=100)  # Field name provided by end user
    field_value = models.TextField(null=True, blank=True)  # Field value provided by end user
    data_type = models.CharField(max_length=20, choices=FIELD_TYPES,null=True,blank =True)
    dropdown_values = models.JSONField(null=True, blank=True)
    radio_values = models.JSONField(null=True, blank=True)
    
    

    def save(self, *args, **kwargs):
        if self.data_type == 'dropdown':
            # Check if dropdown options are provided and valid JSON
            if self.dropdown_values:
                options = self.dropdown_values  # No need for json.loads() here

                # Assign dropdown options to the field_value if it's empty
                if not self.field_value:
                    self.field_value = json.dumps(options)
                else:
                    # If field_value is not empty, check if it's in the dropdown options
                    if self.field_value not in options.values():
                        raise ValueError("Selected value is not in the dropdown options.")

        elif self.data_type == 'radio':
            # If radio options are not provided, use an empty list
            if self.radio_values:
                options = self.radio_values  # No need for json.loads() here

                # Assign radio options to the field_value if it's empty
                if not self.field_value:
                    self.field_value = json.dumps(options)
                else:
                    # If field_value is not empty, check if it's in the radio options
                    if self.field_value not in options.values():
                        raise ValueError("Selected value is not in the radio options.")
        else:
            if isinstance(self.field_value, int) or self.field_value.isdigit():
                self.data_type = 'integer'
            elif isinstance(self.field_value, str):
                if re.match(r'\d{1,2}-\d{1,2}-\d{4}', self.field_value):
                    parts = self.field_value.split('-')
                    # Add leading zeros if necessary
                    day = parts[0].zfill(2)
                    month = parts[1].zfill(2)
                    formatted_date = f"{day}-{month}-{parts[2]}"
                    try:
                        parsed_date = datetime.strptime(formatted_date, '%d-%m-%Y').date()
                    except ValueError:
                        raise ValidationError({'field_value': ['Invalid date format. Date should be in DD-MM-YYYY format.']})
                    self.data_type = 'date'
                    self.date_field = parsed_date
                elif self.field_value.lower() in ['yes', 'no', 'true', 'false', '0', '1']:
                    self.data_type = 'boolean'
                elif re.match(r"[^@]+@[^@]+\.[^@]+", self.field_value):
                    self.data_type = 'email'
                elif self.data_type == 'dropdown':
                    # Parse dropdown options if provided
                    if self.field_value:
                        self.field_value = self.field_value.split(',')
                elif self.data_type == 'radio':
                    # Parse radio options if provided
                    if self.field_value:
                        self.field_value = self.field_value.split(',')
                else:
                    self.data_type = 'text'
            else:
                raise ValueError(f"Invalid value '{self.field_value}' for data type '{self.data_type}'.")
        
        super().save(*args, **kwargs)

#EMPLOPYEE JOB HISTORY
class EmpJobHistory(models.Model):
    emp_id =models.ForeignKey('emp_master',on_delete = models.CASCADE,related_name='emp_job_history')
    emp_sl_no = models.CharField(max_length=50, unique=True,null=False,blank =True,default=None)
    emp_jh_from_date = models.DateField()
    emp_jh_end_date = models.DateField()
    emp_jh_company_name=models.CharField(max_length=50)
    emp_jh_designation = models.CharField(max_length=50)
    emp_jh_leaving_salary_permonth = models.FloatField()
    emp_jh_reason = models.CharField(max_length=100)
    emp_jh_years_experiance = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('UserManagement.CustomUser', on_delete=models.SET_NULL, null=True, related_name='%(class)s_created_by')
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey('UserManagement.CustomUser', on_delete=models.SET_NULL, null=True, related_name='%(class)s_updated_by')

    def __str__(self):
        return f"{self.emp_sl_no }"

class EmpJobHistory_CustomField(models.Model):
    FIELD_TYPES = (
        ('dropdown', 'DropdownField'),
        ('radio', 'RadioButtonField'),)
    emp_job_history = models.ForeignKey(EmpJobHistory, on_delete=models.CASCADE,related_name='jobhistory_customfields')
    field_name = models.CharField(max_length=100)  # Field name provided by end user
    field_value = models.TextField(null=True, blank=True)  # Field value provided by end user
    data_type = models.CharField(max_length=20, choices=FIELD_TYPES,null=True,blank =True)
    dropdown_values = models.JSONField(null=True, blank=True)
    radio_values = models.JSONField(null=True, blank=True)
    
    
    def save(self, *args, **kwargs):
        if self.data_type == 'dropdown':
            # Check if dropdown options are provided and valid JSON
            if self.dropdown_values:
                options = self.dropdown_values  # No need for json.loads() here

                # Assign dropdown options to the field_value if it's empty
                if not self.field_value:
                    self.field_value = json.dumps(options)
                else:
                    # If field_value is not empty, check if it's in the dropdown options
                    if self.field_value not in options.values():
                        raise ValueError("Selected value is not in the dropdown options.")

        elif self.data_type == 'radio':
            # If radio options are not provided, use an empty list
            if self.radio_values:
                options = self.radio_values  # No need for json.loads() here

                # Assign radio options to the field_value if it's empty
                if not self.field_value:
                    self.field_value = json.dumps(options)
                else:
                    # If field_value is not empty, check if it's in the radio options
                    if self.field_value not in options.values():
                        raise ValueError("Selected value is not in the radio options.")
        else:
            if isinstance(self.field_value, int) or self.field_value.isdigit():
                self.data_type = 'integer'
            elif isinstance(self.field_value, str):
                if re.match(r'\d{1,2}-\d{1,2}-\d{4}', self.field_value):
                    parts = self.field_value.split('-')
                    # Add leading zeros if necessary
                    day = parts[0].zfill(2)
                    month = parts[1].zfill(2)
                    formatted_date = f"{day}-{month}-{parts[2]}"
                    try:
                        parsed_date = datetime.strptime(formatted_date, '%d-%m-%Y').date()
                    except ValueError:
                        raise ValidationError({'field_value': ['Invalid date format. Date should be in DD-MM-YYYY format.']})
                    self.data_type = 'date'
                    self.date_field = parsed_date
                elif self.field_value.lower() in ['yes', 'no', 'true', 'false', '0', '1']:
                    self.data_type = 'boolean'
                elif re.match(r"[^@]+@[^@]+\.[^@]+", self.field_value):
                    self.data_type = 'email'
                elif self.data_type == 'dropdown':
                    # Parse dropdown options if provided
                    if self.field_value:
                        self.field_value = self.field_value.split(',')
                elif self.data_type == 'radio':
                    # Parse radio options if provided
                    if self.field_value:
                        self.field_value = self.field_value.split(',')
                else:
                    self.data_type = 'text'
            else:
                raise ValueError(f"Invalid value '{self.field_value}' for data type '{self.data_type}'.")
        
        super().save(*args, **kwargs)




#EMPLOYEE QUALIFICATION
class EmpQualification(models.Model):
    emp_id =models.ForeignKey('emp_master',on_delete = models.CASCADE,related_name='emp_qualification')
    emp_sl_no = models.CharField(max_length=50, unique=True, null=True,blank =True,default=None)
    emp_qualification = models.CharField(max_length=50)
    emp_qf_instituition = models.CharField(max_length=50)
    emp_qf_year = models.DateField()
    emp_qf_subject= models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('UserManagement.CustomUser', on_delete=models.SET_NULL, null=True, related_name='%(class)s_created_by')
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey('UserManagement.CustomUser', on_delete=models.SET_NULL, null=True, related_name='%(class)s_updated_by')

    def __str__(self):
        return f"{self.emp_sl_no }"

class EmpQualification_CustomField(models.Model):
    FIELD_TYPES = (
        ('dropdown', 'DropdownField'),
        ('radio', 'RadioButtonField'),
        )
    emp_qualification = models.ForeignKey(EmpQualification, on_delete=models.CASCADE,related_name='custom_fields')
    field_name = models.CharField(max_length=100)  # Field name provided by end user
    field_value = models.TextField(null=True, blank=True)  # Field value provided by end user
    data_type = models.CharField(max_length=20, choices=FIELD_TYPES,null=True,blank =True)
    dropdown_values = models.JSONField(null=True, blank=True)
    radio_values = models.JSONField(null=True, blank=True)
    
    
    def save(self, *args, **kwargs):
        if self.data_type == 'dropdown':
            # Check if dropdown options are provided and valid JSON
            if self.dropdown_values:
                options = self.dropdown_values  # No need for json.loads() here

                # Assign dropdown options to the field_value if it's empty
                if not self.field_value:
                    self.field_value = json.dumps(options)
                else:
                    # If field_value is not empty, check if it's in the dropdown options
                    if self.field_value not in options.values():
                        raise ValueError("Selected value is not in the dropdown options.")

        elif self.data_type == 'radio':
            # If radio options are not provided, use an empty list
            if self.radio_values:
                options = self.radio_values  # No need for json.loads() here

                # Assign radio options to the field_value if it's empty
                if not self.field_value:
                    self.field_value = json.dumps(options)
                else:
                    # If field_value is not empty, check if it's in the radio options
                    if self.field_value not in options.values():
                        raise ValueError("Selected value is not in the radio options.")
        else:
            if isinstance(self.field_value, int) or self.field_value.isdigit():
                self.data_type = 'integer'
            elif isinstance(self.field_value, str):
                if re.match(r'\d{1,2}-\d{1,2}-\d{4}', self.field_value):
                    parts = self.field_value.split('-')
                    # Add leading zeros if necessary
                    day = parts[0].zfill(2)
                    month = parts[1].zfill(2)
                    formatted_date = f"{day}-{month}-{parts[2]}"
                    try:
                        parsed_date = datetime.strptime(formatted_date, '%d-%m-%Y').date()
                    except ValueError:
                        raise ValidationError({'field_value': ['Invalid date format. Date should be in DD-MM-YYYY format.']})
                    self.data_type = 'date'
                    self.date_field = parsed_date
                elif self.field_value.lower() in ['yes', 'no', 'true', 'false', '0', '1']:
                    self.data_type = 'boolean'
                elif re.match(r"[^@]+@[^@]+\.[^@]+", self.field_value):
                    self.data_type = 'email'
                elif self.data_type == 'dropdown':
                    # Parse dropdown options if provided
                    if self.field_value:
                        self.field_value = self.field_value.split(',')
                elif self.data_type == 'radio':
                    # Parse radio options if provided
                    if self.field_value:
                        self.field_value = self.field_value.split(',')
                else:
                    self.data_type = 'text'
            else:
                raise ValueError(f"Invalid value '{self.field_value}' for data type '{self.data_type}'.")
        
        super().save(*args, **kwargs)




#EMPLOYEE DOCUMENTS
class Emp_Documents(models.Model):
    emp_id =models.ForeignKey('emp_master',on_delete = models.CASCADE,related_name='emp_documents')
    emp_sl_no = models.CharField(max_length=50, unique=True, null=True,blank =True,default=None)
    emp_doc_type = models.ForeignKey("Core.Document_type",on_delete = models.CASCADE,null=True,blank =True)
    emp_doc_number = models.IntegerField()
    emp_doc_issued_date = models.DateField()
    emp_doc_expiry_date = models.DateField()
    emp_doc_document = models.FileField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('UserManagement.CustomUser', on_delete=models.SET_NULL, null=True, related_name='%(class)s_created_by')
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey('UserManagement.CustomUser', on_delete=models.SET_NULL, null=True, related_name='%(class)s_updated_by')

    def __str__(self):
        return f"{self.emp_sl_no }"

class EmpDocuments_CustomField(models.Model):
    FIELD_TYPES = (
        ('dropdown', 'DropdownField'),
        ('radio', 'RadioButtonField'),
        )
    emp_documents = models.ForeignKey(Emp_Documents, on_delete=models.CASCADE,related_name='custom_fields')
    field_name = models.CharField(max_length=100)  # Field name provided by end user
    field_value = models.TextField(null=True, blank=True)  # Field value provided by end user
    data_type = models.CharField(max_length=20, choices=FIELD_TYPES,null=True,blank =True)
    dropdown_values = models.JSONField(null=True, blank=True)
    radio_values = models.JSONField(null=True, blank=True)
    
    
    def save(self, *args, **kwargs):
        if self.data_type == 'dropdown':
            # Check if dropdown options are provided and valid JSON
            if self.dropdown_values:
                options = self.dropdown_values  # No need for json.loads() here

                # Assign dropdown options to the field_value if it's empty
                if not self.field_value:
                    self.field_value = json.dumps(options)
                else:
                    # If field_value is not empty, check if it's in the dropdown options
                    if self.field_value not in options.values():
                        raise ValueError("Selected value is not in the dropdown options.")

        elif self.data_type == 'radio':
            # If radio options are not provided, use an empty list
            if self.radio_values:
                options = self.radio_values  # No need for json.loads() here

                # Assign radio options to the field_value if it's empty
                if not self.field_value:
                    self.field_value = json.dumps(options)
                else:
                    # If field_value is not empty, check if it's in the radio options
                    if self.field_value not in options.values():
                        raise ValueError("Selected value is not in the radio options.")
        else:
            if isinstance(self.field_value, int) or self.field_value.isdigit():
                self.data_type = 'integer'
            elif isinstance(self.field_value, str):
                if re.match(r'\d{1,2}-\d{1,2}-\d{4}', self.field_value):
                    parts = self.field_value.split('-')
                    # Add leading zeros if necessary
                    day = parts[0].zfill(2)
                    month = parts[1].zfill(2)
                    formatted_date = f"{day}-{month}-{parts[2]}"
                    try:
                        parsed_date = datetime.strptime(formatted_date, '%d-%m-%Y').date()
                    except ValueError:
                        raise ValidationError({'field_value': ['Invalid date format. Date should be in DD-MM-YYYY format.']})
                    self.data_type = 'date'
                    self.date_field = parsed_date
                elif self.field_value.lower() in ['yes', 'no', 'true', 'false', '0', '1']:
                    self.data_type = 'boolean'
                elif re.match(r"[^@]+@[^@]+\.[^@]+", self.field_value):
                    self.data_type = 'email'
                elif self.data_type == 'dropdown':
                    # Parse dropdown options if provided
                    if self.field_value:
                        self.field_value = self.field_value.split(',')
                elif self.data_type == 'radio':
                    # Parse radio options if provided
                    if self.field_value:
                        self.field_value = self.field_value.split(',')
                else:
                    self.data_type = 'text'
            else:
                raise ValueError(f"Invalid value '{self.field_value}' for data type '{self.data_type}'.")
        
        super().save(*args, **kwargs)



class EmpLeaveRequest(models.Model):
    employee = models.ForeignKey('emp_master', on_delete=models.CASCADE,related_name='emp_leaverequest')
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=20, default='Pending')
    reason=models.CharField(max_length=150,default='its ook')


class LanguageSkill(models.Model):
    language = models.CharField(max_length=100,null=True,blank =True,default=None)
    
    def __str__(self):
        return f"{self.language }"

class MarketingSkill(models.Model):
    marketing = models.CharField(max_length=100,null=True,blank =True,default=None)

    def __str__(self):
        return f"{self.marketing }"

class ProgrammingLanguageSkill(models.Model):
    programming_language = models.CharField(max_length=100,null=True,blank =True,default=None)

    def __str__(self):
        return f"{self.programming_language }"

class EmployeeSkill(models.Model):
    emp_id =models.ForeignKey('emp_master',on_delete = models.CASCADE,related_name='emp_skills')
    language_skill = models.ForeignKey(LanguageSkill, on_delete=models.SET_NULL, null=True, blank=True)
    marketing_skill = models.ForeignKey(MarketingSkill, on_delete=models.SET_NULL, null=True, blank=True)
    programming_language_skill = models.ForeignKey(ProgrammingLanguageSkill, on_delete=models.SET_NULL, null=True, blank=True)
    value = models.CharField(max_length=100,null=True,blank =True,default=None)
    percentage = models.DecimalField(max_digits=5, decimal_places=2, default=None, null=True, blank=True)

@receiver(pre_save, sender=EmployeeSkill)
def update_value_field(sender, instance, **kwargs):
    if instance.language_skill:
        instance.value = instance.language_skill.language
    elif instance.marketing_skill:
        instance.value = instance.marketing_skill.marketing
    elif instance.programming_language_skill:
        instance.value = instance.programming_language_skill.programming_language


# class Skills_Master(models.Model):
#     emp_id =models.ForeignKey('emp_master',on_delete = models.CASCADE,related_name='emp_skills')
#     language = models.CharField(max_length=100, blank=True, null=True)
#     marketing = models.CharField(max_length=100, blank=True, null=True)
#     programming_language = models.CharField(max_length=100, blank=True, null=True)
#     value = models.JSONField(blank=True, null=True)

#     def save(self, *args, **kwargs):
#         self.value = self.get_selected_values()
#         super().save(*args, **kwargs)


#     def get_selected_values(self):
#         selected_values = {}
#         if self.language:
#             selected_values['language'] = self.get_all_values('language')
#         if self.marketing:
#             selected_values['marketing'] = self.get_all_values('marketing')
#         if self.programming_language:
#             selected_values['programming_language'] = self.get_all_values('programming_language')
#         return selected_values

#     def get_all_values(self, field_name):
#         all_values = Skills_Master.objects.values_list(field_name, flat=True).distinct()
#         return list(all_values)

    
    
    
    
    
    
    
    
    
    

    
