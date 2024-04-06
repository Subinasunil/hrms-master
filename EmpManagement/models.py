
from django.contrib.contenttypes.models import ContentType
from django.db import models
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
    emp_login_id = models.CharField(max_length=50,unique=True,null=True,blank =True)
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
    emp_nationality = models.CharField(null=True,blank =True)
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
                username = self.emp_login_id
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
        return self.emp_login_id or "Unnamed Employee"

class Emp_CustomField(models.Model):
    FIELD_TYPES = (
        ('char', 'CharField'),
        ('date', 'DateField'),
        ('email', 'EmailField'),
        ('integer', 'IntegerField'),
        ('boolean', 'BooleanField'),
        ('dropdown', 'DropdownField'),
        ('text', 'TextField'),
        ('radio', 'RadioButtonField'),
        ('select', 'SelectBoxField'),)
    emp_master = models.ForeignKey(emp_master, on_delete=models.CASCADE,related_name='custom_fields')
    field_name = models.CharField(max_length=100)  # Field name provided by end user
    field_value = models.CharField(max_length=255)  # Field value provided by end user
    data_type = models.CharField(max_length=20, choices=FIELD_TYPES,null=True,blank =True)
    dropdown_values = models.JSONField(null=True, blank=True)
    radio_values = models.JSONField(null=True, blank=True)
    selectbox_values = models.JSONField(null=True, blank=True)
    
    def save(self, *args, **kwargs):
        if self.data_type == 'char':
            self.char_field = self.field_value
        elif self.data_type == 'date':
            try:
                # Corrected date format
                self.date_field = datetime.datetime.strptime(self.field_value, '%d-%m-%Y').date()
            except ValueError:
                raise ValidationError({'field_value': ['Invalid date format. Date should be in DD-MM-YYYY format.']})
        elif self.data_type == 'email':
            self.email_field = self.field_value
            try:
                # Validate email format
                validate_email(self.field_value)
            except ValidationError as e:
                # Raise ValidationError with custom error message
                raise ValidationError({'field_value': ['Invalid email format.']})
            self.email_field = self.field_value
        elif self.data_type == 'integer':
            try:
                # Validate if field_value can be converted to integer
                int(self.field_value)
            except ValueError:
                raise ValidationError({'field_value': ['Invalid integer value.']})
            self.integer_field = int(self.field_value)

        elif self.data_type == 'boolean':
            if self.field_value.lower() in ['true', '1', 'yes']:
                self.boolean_field = True
            elif self.field_value.lower() in ['false', '0', 'no']:
                self.boolean_field = False
            else:
                raise ValidationError({'field_value': ['Invalid boolean value. Accepted values are: true, false, 1, 0, yes, no.']})

        elif self.data_type == 'dropdown':
            try:
                # Split the field_value by comma and store as dropdown values
                dropdown_values_list = [value.strip() for value in self.field_value.split(',')]
                self.dropdown_values = dropdown_values_list
            except Exception as e:
                # Handle exceptions here
                pass
        
        elif self.data_type == 'radio':
            try:
                # Split the field_value by comma and store as radio button values
                radio_values_list = [value.strip() for value in self.field_value.split(',')]
                self.radio_values = radio_values_list
            except Exception as e:
                # Handle exceptions here
                pass

        elif self.data_type == 'select':
            try:
                # Split the field_value by comma and store as select box values
                selectbox_values_list = [value.strip() for value in self.field_value.split(',')]
                self.selectbox_values = selectbox_values_list
            except Exception as e:
                # Handle exceptions here
                pass

        
        elif self.data_type == 'text':
            # Perform validation for text type if needed
            #  check if the length of the text is within acceptable limits
            if len(self.field_value) > 2000:
                raise ValidationError({'field_value': ['Text exceeds maximum length.']})

        super().save(*args, **kwargs)
    
    


#EMPLOYEE FAMILY(ef) data
class emp_family(models.Model):
    emp_id =models.ForeignKey('emp_master',on_delete = models.CASCADE,null=True,blank=True, related_name='emp_family')
    ef_member_name = models.CharField(max_length=50)
    ef_member_no = models.CharField(max_length=50, unique=True,null=False,blank =True,default=None)
    emp_relation = models.CharField(max_length=50)
    ef_company_expence = models.FloatField()
    ef_date_of_birth = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('UserManagement.CustomUser', on_delete=models.SET_NULL, null=True, related_name='%(class)s_created_by')
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey('UserManagement.CustomUser', on_delete=models.SET_NULL, null=True, related_name='%(class)s_updated_by')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.ef_member_no } - {self.emp_login_id}"

class EmpFamily_CustomField(models.Model):
    FIELD_TYPES = (
        ('char', 'CharField'),
        ('date', 'DateField'),
        ('email', 'EmailField'),
        ('integer', 'IntegerField'),
        ('boolean', 'BooleanField'),
        ('dropdown', 'DropdownField'),
        ('text', 'TextField'),
        ('radio', 'RadioButtonField'),
        ('select', 'SelectBoxField'),)
    emp_family = models.ForeignKey('emp_family', on_delete=models.CASCADE, related_name='fam_custom_fields')
    field_name = models.CharField(max_length=100)  # Field name provided by end user
    field_value = models.CharField(max_length=255)  # Field value provided by end user
    data_type = models.CharField(max_length=20, choices=FIELD_TYPES,null=True,blank =True)
    dropdown_values = models.JSONField(null=True, blank=True)
    radio_values = models.JSONField(null=True, blank=True)
    selectbox_values = models.JSONField(null=True, blank=True)
    

    def save(self, *args, **kwargs):
        if self.data_type == 'char':
            self.char_field = self.field_value
        elif self.data_type == 'date':
            try:
                # Corrected date format
                self.date_field = datetime.datetime.strptime(self.field_value, '%d-%m-%Y').date()
            except ValueError:
                raise ValidationError({'field_value': ['Invalid date format. Date should be in DD-MM-YYYY format.']})
        elif self.data_type == 'email':
            self.email_field = self.field_value
            try:
                # Validate email format
                validate_email(self.field_value)
            except ValidationError as e:
                # Raise ValidationError with custom error message
                raise ValidationError({'field_value': ['Invalid email format.']})
            self.email_field = self.field_value
        elif self.data_type == 'integer':
            try:
                # Validate if field_value can be converted to integer
                int(self.field_value)
            except ValueError:
                raise ValidationError({'field_value': ['Invalid integer value.']})
            self.integer_field = int(self.field_value)

        elif self.data_type == 'boolean':
            if self.field_value.lower() in ['true', '1', 'yes']:
                self.boolean_field = True
            elif self.field_value.lower() in ['false', '0', 'no']:
                self.boolean_field = False
            else:
                raise ValidationError({'field_value': ['Invalid boolean value. Accepted values are: true, false, 1, 0, yes, no.']})

        elif self.data_type == 'dropdown':
            try:
                # Split the field_value by comma and store as dropdown values
                dropdown_values_list = [value.strip() for value in self.field_value.split(',')]
                self.dropdown_values = dropdown_values_list
            except Exception as e:
                # Handle exceptions here
                pass
        
        elif self.data_type == 'radio':
            try:
                # Split the field_value by comma and store as radio button values
                radio_values_list = [value.strip() for value in self.field_value.split(',')]
                self.radio_values = radio_values_list
            except Exception as e:
                # Handle exceptions here
                pass

        elif self.data_type == 'select':
            try:
                # Split the field_value by comma and store as select box values
                selectbox_values_list = [value.strip() for value in self.field_value.split(',')]
                self.selectbox_values = selectbox_values_list
            except Exception as e:
                # Handle exceptions here
                pass

        
        elif self.data_type == 'text':
            # Perform validation for text type if needed
            #  check if the length of the text is within acceptable limits
            if len(self.field_value) > 2000:
                raise ValidationError({'field_value': ['Text exceeds maximum length.']})


        super().save(*args, **kwargs)

#EMPLOPYEE JOB HISTORY
class EmpJobHistory(models.Model):
    emp_id =models.ForeignKey('emp_master',on_delete = models.CASCADE,related_name='emp_job_history')
    emp_jh_no = models.CharField(max_length=50, unique=True,null=False,blank =True,default=None)
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
        return f"{self.emp_jh_no }"

class EmpJobHistory_CustomField(models.Model):
    FIELD_TYPES = (
        ('char', 'CharField'),
        ('date', 'DateField'),
        ('email', 'EmailField'),
        ('integer', 'IntegerField'),
        ('boolean', 'BooleanField'),
        ('dropdown', 'DropdownField'),
        ('text', 'TextField'),
        ('radio', 'RadioButtonField'),
        ('select', 'SelectBoxField'),)
    emp_job_history = models.ForeignKey(EmpJobHistory, on_delete=models.CASCADE,related_name='jobhistory_customfields')
    field_name = models.CharField(max_length=100)  # Field name provided by end user
    field_value = models.CharField(max_length=255)  # Field value provided by end user
    data_type = models.CharField(max_length=20, choices=FIELD_TYPES,null=True,blank =True)
    dropdown_values = models.JSONField(null=True, blank=True)
    radio_values = models.JSONField(null=True, blank=True)
    selectbox_values = models.JSONField(null=True, blank=True)
    
    def save(self, *args, **kwargs):
        if self.data_type == 'char':
            self.char_field = self.field_value
        elif self.data_type == 'date':
            try:
                # Corrected date format
                self.date_field = datetime.datetime.strptime(self.field_value, '%d-%m-%Y').date()
            except ValueError:
                raise ValidationError({'field_value': ['Invalid date format. Date should be in DD-MM-YYYY format.']})
        elif self.data_type == 'email':
            self.email_field = self.field_value
            try:
                # Validate email format
                validate_email(self.field_value)
            except ValidationError as e:
                # Raise ValidationError with custom error message
                raise ValidationError({'field_value': ['Invalid email format.']})
            self.email_field = self.field_value
        elif self.data_type == 'integer':
            try:
                # Validate if field_value can be converted to integer
                int(self.field_value)
            except ValueError:
                raise ValidationError({'field_value': ['Invalid integer value.']})
            self.integer_field = int(self.field_value)

        elif self.data_type == 'boolean':
            if self.field_value.lower() in ['true', '1', 'yes']:
                self.boolean_field = True
            elif self.field_value.lower() in ['false', '0', 'no']:
                self.boolean_field = False
            else:
                raise ValidationError({'field_value': ['Invalid boolean value. Accepted values are: true, false, 1, 0, yes, no.']})

        elif self.data_type == 'dropdown':
            try:
                # Split the field_value by comma and store as dropdown values
                dropdown_values_list = [value.strip() for value in self.field_value.split(',')]
                self.dropdown_values = dropdown_values_list
            except Exception as e:
                # Handle exceptions here
                pass
        
        elif self.data_type == 'radio':
            try:
                # Split the field_value by comma and store as radio button values
                radio_values_list = [value.strip() for value in self.field_value.split(',')]
                self.radio_values = radio_values_list
            except Exception as e:
                # Handle exceptions here
                pass

        elif self.data_type == 'select':
            try:
                # Split the field_value by comma and store as select box values
                selectbox_values_list = [value.strip() for value in self.field_value.split(',')]
                self.selectbox_values = selectbox_values_list
            except Exception as e:
                # Handle exceptions here
                pass

        
        elif self.data_type == 'text':
            # Perform validation for text type if needed
            #  check if the length of the text is within acceptable limits
            if len(self.field_value) > 2000:
                raise ValidationError({'field_value': ['Text exceeds maximum length.']})

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
        ('char', 'CharField'),
        ('date', 'DateField'),
        ('email', 'EmailField'),
        ('integer', 'IntegerField'),
        ('boolean', 'BooleanField'),
        ('dropdown', 'DropdownField'),
        ('text', 'TextField'),
        ('radio', 'RadioButtonField'),
        ('select', 'SelectBoxField'),
        )
    emp_qualification = models.ForeignKey(EmpQualification, on_delete=models.CASCADE,related_name='custom_fields')
    field_name = models.CharField(max_length=100)  # Field name provided by end user
    field_value = models.CharField(max_length=255)  # Field value provided by end user
    data_type = models.CharField(max_length=20, choices=FIELD_TYPES,null=True,blank =True)
    dropdown_values = models.JSONField(null=True, blank=True)
    radio_values = models.JSONField(null=True, blank=True)
    selectbox_values = models.JSONField(null=True, blank=True)
    
    def save(self, *args, **kwargs):
        if self.data_type == 'char':
            self.char_field = self.field_value
        elif self.data_type == 'date':
            try:
                # Corrected date format
                self.date_field = datetime.datetime.strptime(self.field_value, '%d-%m-%Y').date()
            except ValueError:
                raise ValidationError({'field_value': ['Invalid date format. Date should be in DD-MM-YYYY format.']})
        elif self.data_type == 'email':
            self.email_field = self.field_value
            try:
                # Validate email format
                validate_email(self.field_value)
            except ValidationError as e:
                # Raise ValidationError with custom error message
                raise ValidationError({'field_value': ['Invalid email format.']})
            self.email_field = self.field_value
        elif self.data_type == 'integer':
            try:
                # Validate if field_value can be converted to integer
                int(self.field_value)
            except ValueError:
                raise ValidationError({'field_value': ['Invalid integer value.']})
            self.integer_field = int(self.field_value)

        elif self.data_type == 'boolean':
            if self.field_value.lower() in ['true', '1', 'yes']:
                self.boolean_field = True
            elif self.field_value.lower() in ['false', '0', 'no']:
                self.boolean_field = False
            else:
                raise ValidationError({'field_value': ['Invalid boolean value. Accepted values are: true, false, 1, 0, yes, no.']})

        elif self.data_type == 'dropdown':
            try:
                # Split the field_value by comma and store as dropdown values
                dropdown_values_list = [value.strip() for value in self.field_value.split(',')]
                self.dropdown_values = dropdown_values_list
            except Exception as e:
                # Handle exceptions here
                pass
        
        elif self.data_type == 'radio':
            try:
                # Split the field_value by comma and store as radio button values
                radio_values_list = [value.strip() for value in self.field_value.split(',')]
                self.radio_values = radio_values_list
            except Exception as e:
                # Handle exceptions here
                pass

        elif self.data_type == 'select':
            try:
                # Split the field_value by comma and store as select box values
                selectbox_values_list = [value.strip() for value in self.field_value.split(',')]
                self.selectbox_values = selectbox_values_list
            except Exception as e:
                # Handle exceptions here
                pass

        
        elif self.data_type == 'text':
            # Perform validation for text type if needed
            #  check if the length of the text is within acceptable limits
            if len(self.field_value) > 2000:
                raise ValidationError({'field_value': ['Text exceeds maximum length.']})


        super().save(*args, **kwargs)




#EMPLOYEE DOCUMENTS
class Emp_Documents(models.Model):
    emp_id =models.ForeignKey('emp_master',on_delete = models.CASCADE,related_name='emp_documents')
    emp_sl_no = models.CharField(max_length=50, unique=True, null=True,blank =True,default=None)
    emp_doc_name = models.CharField(max_length=50)
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
        ('char', 'CharField'),
        ('date', 'DateField'),
        ('email', 'EmailField'),
        ('integer', 'IntegerField'),
        ('boolean', 'BooleanField'),
        ('dropdown', 'DropdownField'),
        ('text', 'TextField'),
        ('radio', 'RadioButtonField'),
        ('select', 'SelectBoxField'),)
    emp_documents = models.ForeignKey(Emp_Documents, on_delete=models.CASCADE,related_name='custom_fields')
    field_name = models.CharField(max_length=100)  # Field name provided by end user
    field_value = models.CharField(max_length=255)  # Field value provided by end user
    data_type = models.CharField(max_length=20, choices=FIELD_TYPES,null=True,blank =True)
    dropdown_values = models.JSONField(null=True, blank=True)
    radio_values = models.JSONField(null=True, blank=True)
    selectbox_values = models.JSONField(null=True, blank=True)
    
    def save(self, *args, **kwargs):
        if self.data_type == 'char':
            self.char_field = self.field_value
        elif self.data_type == 'date':
            try:
                # Corrected date format
                self.date_field = datetime.datetime.strptime(self.field_value, '%d-%m-%Y').date()
            except ValueError:
                raise ValidationError({'field_value': ['Invalid date format. Date should be in DD-MM-YYYY format.']})
        elif self.data_type == 'email':
            self.email_field = self.field_value
            try:
                # Validate email format
                validate_email(self.field_value)
            except ValidationError as e:
                # Raise ValidationError with custom error message
                raise ValidationError({'field_value': ['Invalid email format.']})
            self.email_field = self.field_value
        elif self.data_type == 'integer':
            try:
                # Validate if field_value can be converted to integer
                int(self.field_value)
            except ValueError:
                raise ValidationError({'field_value': ['Invalid integer value.']})
            self.integer_field = int(self.field_value)

        elif self.data_type == 'boolean':
            if self.field_value.lower() in ['true', '1', 'yes']:
                self.boolean_field = True
            elif self.field_value.lower() in ['false', '0', 'no']:
                self.boolean_field = False
            else:
                raise ValidationError({'field_value': ['Invalid boolean value. Accepted values are: true, false, 1, 0, yes, no.']})
        elif self.data_type == 'dropdown':
            try:
                # Split the field_value by comma and store as dropdown values
                dropdown_values_list = [value.strip() for value in self.field_value.split(',')]
                self.dropdown_values = dropdown_values_list
            except Exception as e:
                # Handle exceptions here
                pass
        
        elif self.data_type == 'radio':
            try:
                # Split the field_value by comma and store as radio button values
                radio_values_list = [value.strip() for value in self.field_value.split(',')]
                self.radio_values = radio_values_list
            except Exception as e:
                # Handle exceptions here
                pass

        elif self.data_type == 'select':
            try:
                # Split the field_value by comma and store as select box values
                selectbox_values_list = [value.strip() for value in self.field_value.split(',')]
                self.selectbox_values = selectbox_values_list
            except Exception as e:
                # Handle exceptions here
                pass

        
        elif self.data_type == 'text':
            # Perform validation for text type if needed
            #  check if the length of the text is within acceptable limits
            if len(self.field_value) > 2000:
                raise ValidationError({'field_value': ['Text exceeds maximum length.']})


        super().save(*args, **kwargs)



class EmpLeaveRequest(models.Model):
    employee = models.ForeignKey('emp_master', on_delete=models.CASCADE,related_name='emp_leaverequest')
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=20, default='Pending')
    reason=models.CharField(max_length=150,default='its ook')



    
