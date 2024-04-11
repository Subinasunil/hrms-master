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
    
    class Meta:
        model = Emp_CustomField
        fields = ('id','emp_master','field_name','field_value', 'data_type','dropdown_values','radio_values','selectbox_values') 
    
    def validate_date_format(self, field_value):
        try:
            # Attempt to parse the date string with the expected format 'DD-MM-YYYY'
            parsed_date = datetime.strptime(field_value, '%d-%m-%Y')
        except ValueError:
            raise ValidationError("Invalid date format. Date should be in DD-MM-YYYY format.")

    
    def before_import_row(self, row, **kwargs):
        errors = []

        # Validate emp_master
        emp_master_id = row.get('emp_master')
        if not emp_master.objects.filter(id=emp_master_id).exists():
            errors.append(f"emp_master matching query does not exist for ID: {emp_master_id}")

        # Validate data_type field
        data_type = row.get('data_type')
        if data_type not in ['char', 'email', 'date', 'integer', 'boolean','dropdown', 'text', 'radio', 'select']:
            errors.append("Invalid value for data_type field. Allowed values are 'char', 'email', 'date', 'integer', 'boolean','dropdown', 'text', 'radio', 'select'")

        # Validate field_value based on data_type
        field_value = row.get('field_value')
        dropdown_values = row.get('dropdown_values')
        if data_type == 'dropdown' and field_value and dropdown_values:
            field_values_set = set(value.strip() for value in field_value.split(','))
            dropdown_values_set = set(eval(dropdown_values))
            print(f"Field value set: {field_values_set}")
            print(f"Dropdown values set: {dropdown_values_set}")
            # Check if any value in field_value matches a value in dropdown_values
            if not field_values_set.intersection(dropdown_values_set):
                errors.append("None of the values in field_value match dropdown_values.")
        

        # Validate field_value based on data_type
        data_type = row.get('data_type')
        field_value = row.get('field_value')
        data_type = row.get('data_type')
        field_value = row.get('field_value')

        if data_type == 'date':
            try:
                self.validate_date_format(field_value)
            except ValidationError as e:
                errors.extend(e.messages)
        
        if errors:
            raise ValidationError(errors)
        # if data_type == 'integer':
        #     try:
        #         int(field_value)
        #     except ValueError:
        #         errors.append(f"Field value '{field_value}' is not a valid integer for data type 'integer'.")

        # elif data_type == 'boolean':
        #     if field_value.lower() not in ['true', 'false']:
        #         errors.append(f"Field value '{field_value}' is not a valid boolean value for data type 'boolean'.")

        # elif data_type == 'date':
        #     try:
        #         datetime.strptime(field_value, '%d-%m-%y')
        #     except ValueError:
        #         errors.append(f"Field value '{field_value}' is not a valid date format (YYYY-MM-DD) for data type 'date'.")


        # # Validate date field format for 'field_value'
        # date_format_excel = '%Y-%m-%d %H:%M:%S'  # Format from Excel: YYYY-MM-DD HH:MM:SS
        # date_format = '%d-%m-%Y'  # Format: dd-mm-yyyy
        # field_value = str(row.get('field_value'))  # Convert to string
        # print("Field value:", field_value)  # Add debug print
        # if field_value:
        #     try:
        #         # Convert Excel date format to expected date format
        #         field_value_converted = datetime.strptime(field_value, date_format_excel).strftime(date_format)
        #         # Validate the converted date value
        #         datetime.strptime(field_value_converted, date_format)
        #     except ValueError:
        #         errors.append({"field_value": ["Invalid date format. Date should be in DD-MM-YYYY format."]})
        # else:
        #     errors.append({"field_value": ["Date value for field_value is empty"]})
                
        # if field_value:
        #     if data_type == 'char' and not isinstance(field_value, str):
        #         errors.append("Invalid field_value for char data type. Expected string.")
        #     elif data_type == 'email' and not isinstance(field_value, str):
        #         errors.append("Invalid field_value for email data type. Expected string.")
            
            # elif data_type == 'date':
            #     date_format = '%d-%m-%y'  # Format: dd-mm-yy
            #     try:
            #         if isinstance(date_value, datetime):  # Check if value is already a datetime object
            #             date_value = date_value.strftime('%d-%m-%y')  # Convert datetime object to string
            #         datetime.strptime(date_value, date_format)
            #     except ValueError:
            #         errors.append(f"Invalid date format . Date should be in format dd-mm-yy")
                                                
            # elif data_type == 'integer':
            #     try:
            #         int(field_value)
            #     except ValueError:
            #         errors.append("Invalid field_value for integer data type. Expected integer value.")
            # elif data_type == 'boolean' and field_value not in ['TRUE', 'FALSE', 'true', 'false', '1', '0','yes','no']:
            #     errors.append("Invalid field_value for boolean data type. Expected 'True', 'False', 'true', 'false', '1','0','yes','no'")

            # elif data_type == 'dropdown' and field_value not in dropdown_values:
            #     errors.append("Value in 'field_value' must be one of the values listed in 'dropdown_values'.")

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

    