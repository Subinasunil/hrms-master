from import_export import resources,fields
from datetime import datetime
from .models import emp_master, Emp_CustomField,Emp_Documents
from import_export.widgets import DateWidget
from import_export.widgets import Widget
from django.core.exceptions import ValidationError
from django.db import models
import re
from Core.models import Document_type
from OrganisationManager.models import cmpny_mastr,brnch_mstr



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
    emp_login_id = fields.Field(attribute='emp_login_id', column_name='Employee Code')
    emp_first_name = fields.Field(attribute='emp_first_name', column_name='Employee First Name')
    emp_last_name = fields.Field(attribute='emp_last_name', column_name='Employee Last Name')
    emp_gender = fields.Field(attribute='emp_gender', column_name='Employee Gender')
    emp_date_of_birth = fields.Field(attribute='emp_date_of_birth', column_name='Employee DOB(DD/MM/YYYY)',widget=DateWidget(format='%d/%m/%Y'))
    emp_personal_email = fields.Field(attribute='emp_personal_email', column_name='Employee Personal Email ID')
    is_ess = fields.Field(attribute='is_ess', column_name='Iss ESS (True/False)')
    emp_mobile_number_1 = fields.Field(attribute='emp_mobile_number_1', column_name='Employee Personal Mob No')
    emp_mobile_number_2 = fields.Field(attribute='emp_mobile_number_2', column_name='Employee Company Mobile No')
    emp_country_id = fields.Field(attribute='emp_country_id', column_name='Employee Country Code')
    emp_state_id = fields.Field(attribute='emp_state_id', column_name='Employee State')
    emp_city = fields.Field(attribute='emp_city', column_name='Employee City')
    emp_permenent_address = fields.Field(attribute='emp_permenent_address', column_name='Employee Permanent Address')
    emp_present_address = fields.Field(attribute='emp_present_address', column_name='Employee Current Address')
    emp_status = fields.Field(attribute='emp_status', column_name='Employee Status(True/False)')
    emp_hired_date = fields.Field(attribute='emp_hired_date', column_name='Employee Joining Date(DD/MM/YYYY)')
    emp_active_date = fields.Field(attribute='emp_active_date', column_name='Employee Confirmaton Date(DD/MM/YYYY)')
    emp_relegion = fields.Field(attribute='emp_relegion', column_name='Employee Religion')
    emp_profile_pic = fields.Field(attribute='emp_profile_pic', column_name='Employee Profile Picture')
    emp_blood_group = fields.Field(attribute='emp_blood_group', column_name='Employee Blood Group')
    emp_nationality = fields.Field(attribute='emp_nationality', column_name='Employee Nationality')
    emp_marital_status = fields.Field(attribute='emp_marital_status', column_name='Employee Marital Status')
    emp_father_name = fields.Field(attribute='emp_father_name', column_name='Employee Father Name')
    emp_mother_name = fields.Field(attribute='emp_mother_name', column_name='Employee Mother Name')
    emp_posting_location = fields.Field(attribute='emp_posting_location', column_name='Employee Work Location')
    created_at = fields.Field(attribute='created_at', column_name='Created At')
    created_by = fields.Field(attribute='created_by', column_name='Created By')
    updated_at = fields.Field(attribute='updated_at', column_name='Updated At')
    updated_by = fields.Field(attribute='updated_by', column_name='Updated By')
    is_active = fields.Field(attribute='is_active', column_name='Employee Active(True/False)')
    epm_ot_applicable = fields.Field(attribute='epm_ot_applicable', column_name='Employee OT applicable(True/False)')
    emp_company_id = fields.Field(attribute='emp_company_id', column_name='Employee Company Code')
    emp_branch_id = fields.Field(attribute='emp_branch_id', column_name='Employee Branch Code')
    emp_dept_id = fields.Field(attribute='emp_dept_id', column_name='Employee Department Code')
    emp_desgntn_id = fields.Field(attribute='emp_desgntn_id', column_name='Employee Designation Code')
    emp_ctgry_id = fields.Field(attribute='emp_ctgry_id', column_name='Employee Category Code')
    emp_languages = fields.Field(attribute='emp_languages', column_name='Languages')

    
    
    
    class Meta:
        model = emp_master
        skip_unchanged = True
        report_skipped = False
       
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
        login_id = row.get('Employee Code')
        mobile_number_1 = row.get('Employee Personal Mob No')
        mobile_number_2 = row.get('Employee Company Mobile No')
        personal_email = row.get('Employee Personal Email ID')

        
        if emp_master.objects.filter(emp_login_id=login_id).exists():
            errors.append(f"Duplicate value found for Employee Code: {login_id}")
            print(login_id)
            
        if emp_master.objects.filter(emp_mobile_number_1=mobile_number_1).exists():
            errors.append(f"Duplicate value found for Employee Company Mobile No: {mobile_number_1}")
            print(mobile_number_1)

        if mobile_number_2 and emp_master.objects.filter(emp_mobile_number_2=mobile_number_2).exists():
            errors.append(f"Duplicate value found for Employee Personal Email ID: {mobile_number_2}")

        if emp_master.objects.filter(emp_personal_email=personal_email).exists():
            errors.append(f"Duplicate value found for Employee Personal Email ID: {personal_email}")
        print(personal_email)
         # Validating gender field
        gender = row.get('Employee Gender')
        if gender and gender not in ['Male', 'Female', 'Other', 'M', 'F', 'O']:
            errors.append("Invalid value for Employee Gender field. Allowed values are 'Male', 'Female', 'Other', 'M', 'F', or 'O'")
        
        mobile_number_1 = row.get('Employee Personal Mob No')
        if mobile_number_1:
            try:
                NumericMobileNumberWidget().clean(mobile_number_1)
            except ValidationError as e:
                errors.append(str(e))

        mobile_number_2 = row.get('Employee Company Mobile No')
        if mobile_number_2:
            try:
                NumericMobileNumberWidget().clean(mobile_number_2)
            except ValidationError as e:
                errors.append(str(e))

        # Validate date fields format
        date_fields = ['Employee DOB(DD/MM/YYYY)', 'Employee Joining Date(DD/MM/YYYY)', 'Employee Confirmaton Date(DD/MM/YYYY)']
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
        email = row.get('Employee Personal Email ID')
        if email:
            if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
                errors.append(f"Invalid email format for Employee Personal Email ID' field:{email}")

        
        # Validating marital status field
        marital_status = row.get('Employee Marital Status')
        if marital_status and marital_status not in ['Single', 'Married', 'Other', 'S', 'M', 'D']:
            errors.append("Invalid value for marital status field. Allowed values are 'Single', 'Married', 'Other', 'S', 'M', or 'D'")            
        # Get foreign key values from the row
        # company_id = row.get('Employee Company Code')

        # # Validate and retrieve company instance
        # try:
        #     company_instance = cmpny_mastr.objects.get(id=company_id)
        # except cmpny_mastr.DoesNotExist:
        #     errors.append(f"Company with ID '{company_id}' does not exist.")
        #     raise ValidationError(errors)

        # # Assign company instance to the row
        # row['emp_company_id'] = company_instance
        # if errors:
        #     raise ValidationError(errors)


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
            raise ValidationError(f"emp_master matching query does not exist for ID: {emp_master_id}")
        
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
        fields = ('id', 'emp_master', 'field_name', 'field_value') 
    
class DocumentResource(resources.ModelResource):
    # emp_id = fields.Field(attribute='emp_id', column_name='Employee ID')
    # emp_sl_no = fields.Field(attribute='emp_sl_no', column_name='SerialNo')
    # emp_doc_type = fields.Field(attribute='emp_doc_type', column_name='Document Type')
    # emp_doc_number = fields.Field(attribute='emp_doc_number', column_name='Document Number')
    # emp_doc_issued_date = fields.Field(attribute='emp_doc_issued_date', column_name='Document Issued Date')
    # emp_doc_expiry_date = fields.Field(attribute='emp_doc_expiry_date', column_name='Document Expiry Date')

    
    class Meta:
        model = Emp_Documents
        # skip_unchanged = True
        # report_skipped = False
       
        fields = ('id',
                  'emp_id',
                  'emp_sl_no',
                  'emp_doc_type',
                  'emp_doc_number',
                  'emp_doc_issued_date',
                  'emp_doc_expiry_date',
        )
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.errors = []

    def before_import_row(self, row, **kwargs):
        errors = []
        
        
        employee_id = row.get('emp_id')
        doc_type_id = row.get('emp_doc_type')
        
        # Validate emp_id and emp_doc_type
        if not emp_master.objects.filter(id=employee_id).exists():
            errors.append(f"emp_master matching query does not exist for ID: {employee_id}")
            # row_errors['emp_id'] = f"emp_master matching query does not exist for ID: {employee_id}"
        if not Document_type.objects.filter(id=doc_type_id).exists():
            errors.append(f"Document_type matching query does not exist for ID: {doc_type_id}")
            
        
        # Validate date fields format
        date_fields = ['emp_doc_issued_date', 'emp_doc_expiry_date']
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
                

        
        if errors:
            raise ValidationError(errors)


       





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

    