
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from UserManagement.serializers import CustomUserSerializer
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
import pandas as pd


from .models import (emp_family,EmpJobHistory,EmpQualification,Emp_Documents,EmpLeaveRequest,emp_master,Emp_CustomField,
                    EmpFamily_CustomField,EmpJobHistory_CustomField,EmpQualification_CustomField,EmpDocuments_CustomField)

'''employee set'''

 

#EMPLOYEE FAMILY
class EmpFam_CustomFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmpFamily_CustomField
        fields = '__all__'  

class EmpFamSerializer(serializers.ModelSerializer):
    fam_custom_fields = EmpFam_CustomFieldSerializer(many=True, read_only=True)
    created_by = serializers.HiddenField(default=serializers.CurrentUserDefault())
    updated_by = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model= emp_family
        fields = '__all__' 
    def to_representation(self, instance):
        rep = super(EmpFamSerializer, self).to_representation(instance)
        if instance.emp_id:  # Check if emp_state_id is not None
            rep['emp_id'] = instance.emp_id.emp_first_name + " " + instance.emp_id.emp_last_name
        return rep
#experiance

class EmpJobHistory_Udf_Serializer(serializers.ModelSerializer):
    class Meta:
        model = EmpJobHistory_CustomField
        fields = '__all__' 


class EmpJobHistorySerializer(serializers.ModelSerializer):
    jobhistory_customfields = EmpJobHistory_Udf_Serializer(many=True, read_only=True)
    created_by = serializers.HiddenField(default=serializers.CurrentUserDefault())
    updated_by = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model= EmpJobHistory
        fields = '__all__' 
    def to_representation(self, instance):
        rep = super(EmpJobHistorySerializer, self).to_representation(instance)
        if instance.emp_id:  # Check if emp_state_id is not None
            rep['emp_id'] = instance.emp_id.emp_first_name + " " + instance.emp_id.emp_last_name
        return rep
 

#EMPLOYEE QUALIFICATION CREDENTIALS

class Emp_qf_udf_Serializer(serializers.ModelSerializer):
    class Meta:
        model = EmpQualification_CustomField
        fields = '__all__'  


class Emp_qf_Serializer(serializers.ModelSerializer):
    custom_fields = Emp_qf_udf_Serializer(many=True, read_only=True)
    created_by = serializers.HiddenField(default=serializers.CurrentUserDefault())
    updated_by = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = EmpQualification
        fields = '__all__' 
    def to_representation(self, instance):
        rep = super(Emp_qf_Serializer, self).to_representation(instance)
        if instance.emp_id:  # Check if emp_state_id is not None
            rep['emp_id'] = instance.emp_id.emp_first_name + " " + instance.emp_id.emp_last_name
        return rep
 

#EMPLOYEE DOCUMENT CREDENTIALS

class EmpDocuments_Udf_Serializer(serializers.ModelSerializer):
    class Meta:
        model = EmpDocuments_CustomField
        fields = '__all__'


class DocumentSerializer(serializers.ModelSerializer):
    custom_fields = EmpDocuments_Udf_Serializer(many=True, read_only=True)
    created_by = serializers.HiddenField(default=serializers.CurrentUserDefault())
    updated_by = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = Emp_Documents
        fields = '__all__' 
    def to_representation(self, instance):
        rep = super(DocumentSerializer, self).to_representation(instance)
        if instance.emp_id:  # Check if emp_state_id is not None
            rep['emp_id'] = instance.emp_id.emp_first_name + " " + instance.emp_id.emp_last_name
        return rep

class DocBulkuploadSerializer(serializers.ModelSerializer):
    file = serializers.FileField(write_only=True) 
    class Meta:
        model = Emp_Documents
        fields = '__all__'




# EMPLOYEE LEAVE REQUEST

class EmpLeaveRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmpLeaveRequest
        fields = '__all__' 
    def to_representation(self, instance):
        rep = super(EmpLeaveRequestSerializer, self).to_representation(instance)
        if instance.employee:  # Check if emp_state_id is not None
            rep['employee'] = instance.employee.emp_first_name + " " + instance.employee.emp_last_name
        return rep
"""employee"""


class CustomFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = Emp_CustomField
        fields = '__all__' 

    def validate_field_value(self, value):
        data_type = self.initial_data.get('data_type')
        if data_type:
            if data_type == 'integer':
                try:
                    int(value)
                except ValueError:
                    raise ValidationError("Field value must be an integer.")

            elif data_type == 'email':
                
                try:
                    validate_email(value)
                except ValidationError:
                    raise ValidationError("Invalid email address.")

            elif data_type == 'boolean':
                if value.lower() not in ['true', 'false']:
                    raise ValidationError("Field value must be 'true' or 'false'.")

            elif data_type == 'date':
                from datetime import datetime
                try:
                    datetime.strptime(value, '%d-%m-%Y')
                except ValueError:
                    raise ValidationError("Date must be in the format dd-mm-yyyy.")

        return value
            

#EMPLOYEE SERIALIZER
class EmpSerializer(serializers.ModelSerializer):
    
    # user = CustomUserSerializer()
    emp_family = EmpFamSerializer(many=True, read_only=True)
    emp_documents = DocumentSerializer(many=True, read_only=True)
    emp_qualification = Emp_qf_Serializer(many=True, read_only=True)
    emp_job_history = EmpJobHistorySerializer(many=True, read_only=True)
    custom_fields = CustomFieldSerializer(many=True, read_only=True)
    

    created_by = serializers.HiddenField(default=serializers.CurrentUserDefault())
    updated_by = serializers.HiddenField(default=serializers.CurrentUserDefault())
    # file = serializers.FileField(write_only=True)
    class Meta:
        model = emp_master
        fields = '__all__' 
    
    
        
    def to_representation(self, instance):
        rep = super(EmpSerializer, self).to_representation(instance)
        if instance.emp_state_id:  # Check if emp_state_id is not None
            rep['emp_state_id'] = instance.emp_state_id.state_name
        if instance.emp_country_id:  
            rep['emp_country_id'] = instance.emp_country_id.country_name
        if instance.emp_company_id:  
            rep['emp_company_id'] = instance.emp_company_id.cmpny_name
        if instance.emp_dept_id:  
            rep['emp_dept_id'] = instance.emp_dept_id.dept_name
        if instance.emp_languages.exists():
            rep['emp_languages'] = [language.language for language in instance.emp_languages.all()]
        return rep





class EmpBulkUploadSerializer(serializers.ModelSerializer):
    emp_custom_fields = CustomFieldSerializer(many=True, required=False)
    file = serializers.FileField(write_only=True) 
    class Meta:
        model = emp_master
        fields = '__all__'

    def create(self, validated_data):
        custom_fields_data = validated_data.pop('emp_custom_fields', [])
        instance = super().create(validated_data)
        for custom_field_data in custom_fields_data:
            Emp_CustomField.objects.create(emp_family=instance, **custom_field_data)
        return instance

    