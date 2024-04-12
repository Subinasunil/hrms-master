from import_export import resources,fields
from datetime import datetime
from .models import emp_master, Emp_CustomField
from import_export.widgets import DateWidget
from import_export.widgets import Widget
from django.core.exceptions import ValidationError
from django.db import models
import re



class NumericMobileNumberWidget(Widget):   
    def clean(self, value, row=None, *args, **kwargs):
        # Clean the value - convert it to an integer.    
        if value:
            try:
                return int(value)
            except ValueError:
                raise ValidationError("Mobile number must be numeric.")
        return None

class EmployeeResource(resources.ModelResource):
    class Meta:
        model = emp_master
       
        fields = ('id',
            'emp_login_id',
            'emp_first_name',
            'emp_last_name',
            'emp_gender',
            'emp_date_of_birth',
            'emp_personal_email',
            'is_ess',
            'emp_mobile_number_1',
            'emp_mobile_number_2',
            'emp_country_id',
            'emp_state_id',
            'emp_city',
            'emp_permenent_address',
            'emp_present_address',
            'emp_status',
            'emp_hired_date',
            'emp_active_date',
            'emp_relegion',
            'emp_profile_pic',
            'emp_blood_group',
            'emp_nationality',
            'emp_marital_status',
            'emp_father_name',
            'emp_mother_name',
            'emp_posting_location',
            'created_at',
            'created_by',
            'updated_at',
            'updated_by',
            'is_active',
            'epm_ot_applicable',
            'emp_company_id',
            'emp_branch_id',
            'emp_dept_id',
            'emp_desgntn_id',
            'emp_ctgry_id',
            # Many-to-Many field
            'emp_languages',
        )

    

    def before_import_row(self, row, **kwargs):
        errors = []
        login_id = row.get('emp_login_id')
        mobile_number_1 = row.get('emp_mobile_number_1')
        mobile_number_2 = row.get('emp_mobile_number_2')
        personal_email = row.get('emp_personal_email')

        
        if emp_master.objects.filter(emp_login_id=login_id).exists():
            errors.append(f"Duplicate value found for emp_login_id: {login_id}")

        if emp_master.objects.filter(emp_mobile_number_1=mobile_number_1).exists():
            errors.append(f"Duplicate value found for emp_mobile_number_1: {mobile_number_1}")

        if mobile_number_2 and emp_master.objects.filter(emp_mobile_number_2=mobile_number_2).exists():
            errors.append(f"Duplicate value found for emp_mobile_number_2: {mobile_number_2}")

        if emp_master.objects.filter(emp_personal_email=personal_email).exists():
            errors.append(f"Duplicate value found for emp_personal_email: {personal_email}")

         # Validating gender field
        gender = row.get('emp_gender')
        if gender and gender not in ['Male', 'Female', 'Other', 'M', 'F', 'O']:
            errors.append("Invalid value for gender field. Allowed values are 'Male', 'Female', 'Other', 'M', 'F', or 'O'")
        
        mobile_number_1 = row.get('emp_mobile_number_1')
        if mobile_number_1:
            try:
                NumericMobileNumberWidget().clean(mobile_number_1)
            except ValidationError as e:
                errors.append(str(e))

        mobile_number_2 = row.get('emp_mobile_number_2')
        if mobile_number_2:
            try:
                NumericMobileNumberWidget().clean(mobile_number_2)
            except ValidationError as e:
                errors.append(str(e))

        # Validate date fields format
        date_fields = ['emp_date_of_birth', 'emp_hired_date', 'emp_active_date']
        date_format = '%d-%m-%y'  # Format: dd-mm-yy

        for field in date_fields:
            date_value = row.get(field)
            if date_value:
                try:
                    if isinstance(date_value, datetime):  # Check if value is already a datetime object
                        date_value = date_value.strftime('%d-%m-%y')  # Convert datetime object to string
                    datetime.strptime(date_value, date_format)
                except ValueError:
                    errors.append(f"Invalid date format for {field}. Date should be in format dd-mm-yy")
            else:
                errors.append(f"Date value for {field} is empty")
        # Validate email format
        email = row.get('emp_personal_email')
        if email:
            if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
                errors.append(f"Invalid email format for emp_personal_email field:{email}")

        
        # Validating marital status field
        marital_status = row.get('emp_marital_status')
        if marital_status and marital_status not in ['Single', 'Married', 'Other', 'S', 'M', 'D']:
            errors.append("Invalid value for marital status field. Allowed values are 'Single', 'Married', 'Other', 'S', 'M', or 'D'")            
        
        if errors:
            raise ValidationError(errors)


class EmpCustomFieldResource(resources.ModelResource):
    TEXT_LIMIT_MIN = 1000
    TEXT_LIMIT_MAX = 1000000
    DATE_FORMAT = '%d-%m-%Y'

    def __init__(self):
        self.errors = []

    def before_import_row(self, row, row_idx=None, **kwargs):
        field_value = row.get('field_value')
        emp_master_id = row.get('emp_master')

        if field_value is None:
            row['field_value'] = ""
            return

        if isinstance(field_value, int) or field_value.isdigit():
            row['field_value'] = int(field_value)
        elif isinstance(field_value, str):
            if re.match(r'\d{2}-\d{2}-\d{4}', field_value):
                parsed_date = datetime.strptime(field_value, self.DATE_FORMAT).date()
                row['field_value'] = parsed_date
            elif field_value.lower() in ['yes', 'no', 'true', 'false', '0', '1']:
                row['field_value'] = field_value.lower() in ['true', '1']
            elif re.match(r"[^@]+@[^@]+\.[^@]+", field_value):
                row['field_value'] = field_value
            elif len(field_value) > self.TEXT_LIMIT_MIN or ',' in field_value:
                row['field_value'] = field_value
            else:
                row['field_value'] = field_value
        else:
            raise ValueError(f"Invalid value '{field_value}' in row {row_idx}. Expected int, str, or None.")
        
        if not emp_master.objects.filter(id=emp_master_id).exists():
            self.errors.append({'row_idx': row_idx, 'error': f"emp_master matching query does not exist for ID: {emp_master_id}"})
        
    def after_import_row(self, row, row_result, **kwargs):
        if row_result.errors:
            self.errors.append({'row_idx': row_result.row_idx, 'errors': row_result.errors})
        elif row_result.instance is not None and hasattr(row_result.instance, 'field_value') and isinstance(row_result.instance.field_value, datetime):
            row_result.instance.field_value = row_result.instance.field_value.date()

    def before_import(self, dataset, using_transactions, dry_run, **kwargs):
        for row_idx, row in enumerate(dataset.dict, start=2):
            field_value = row.get('field_value')
            if field_value is not None and isinstance(field_value, str):
                if not re.match(r'\d{2}-\d{2}-\d{4}', field_value):
                    self.errors.append({'row_idx': row_idx, 'errors': [f"Invalid date format '{field_value}'. Please use 'dd-mm-yyyy' format."]})
    
    
    class Meta:
        model = Emp_CustomField
        fields = ('id','emp_master','field_name','field_value') 
    
   


class EmpResource_Export(resources.ModelResource):
    class Meta:
        model = emp_master
       
        fields = ('id',
            'emp_login_id',
            'emp_first_name',
            'emp_last_name',
            'emp_gender',
            'emp_date_of_birth',
            'emp_personal_email',
            'is_ess',
            'emp_mobile_number_1',
            'emp_mobile_number_2',
            'emp_country_id',
            'emp_state_id',
            'emp_city',
            'emp_permenent_address',
            'emp_present_address',
            'emp_status',
            'emp_hired_date',
            'emp_active_date',
            'emp_relegion',
            'emp_profile_pic',
            'emp_blood_group',
            'emp_nationality',
            'emp_marital_status',
            'emp_father_name',
            'emp_mother_name',
            'emp_posting_location',
            'created_at',
            'created_by',
            'updated_at',
            'updated_by',
            'is_active',
            'epm_ot_applicable',
            'emp_company_id',
            'emp_branch_id',
            'emp_dept_id',
            'emp_desgntn_id',
            'emp_ctgry_id',
            # Many-to-Many field
            'emp_languages',
        )

    