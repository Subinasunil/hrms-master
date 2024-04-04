from .models import (brnch_mstr,cmpny_mastr,dept_master,desgntn_master,
                     ctgry_master,LanguageMaster,FiscalPeriod,FiscalYear)
from rest_framework import serializers

class BranchSerializer(serializers.ModelSerializer):
    br_created_by = serializers.HiddenField(default=serializers.CurrentUserDefault())
    br_updated_by = serializers.HiddenField(default=serializers.CurrentUserDefault())
    # file = serializers.FileField(write_only=True)
    class Meta:
        model = brnch_mstr
        fields = '__all__'
    def to_representation(self, instance):
        rep = super(BranchSerializer, self).to_representation(instance)
        rep['br_state_id'] = instance.br_state_id.state_name
        rep['br_country'] = instance.br_country.country_name
        rep['br_company_id'] = instance.br_company_id.cmpny_name
        return rep

class BranchuploadSerializer(serializers.ModelSerializer):
    file = serializers.FileField(write_only=True)
    class Meta:
        model = brnch_mstr
        fields = '__all__'




class CompanySerializer(serializers.ModelSerializer):
    cmpny_created_by = serializers.HiddenField(default=serializers.CurrentUserDefault())
    cmpny_updated_by = serializers.HiddenField(default=serializers.CurrentUserDefault())
    branches = BranchSerializer(many=True, read_only=True)
    # file = serializers.FileField(write_only=True)
    class Meta:
        model = cmpny_mastr
        fields = '__all__'
    def to_representation(self, instance):
        rep = super(CompanySerializer, self).to_representation(instance)
        rep['cmpny_state_id'] = instance.cmpny_state_id.state_name
        rep['cmpny_country'] = instance.cmpny_country.country_name
        return rep

#DEPARTMENT SERIALIZER
class DeptSerializer(serializers.ModelSerializer):
    created_by = serializers.HiddenField(default=serializers.CurrentUserDefault())
    updated_by = serializers.HiddenField(default=serializers.CurrentUserDefault())
    # file = serializers.FileField(write_only=True)
    class Meta:
        model = dept_master
        fields= '__all__'
    def to_representation(self, instance):
        rep = super(DeptSerializer, self).to_representation(instance)
        rep['branch_id'] = instance.branch_id.branch_name
        return rep

class DeptUploadSerializer(serializers.ModelSerializer):
    file = serializers.FileField(write_only=True)
    class Meta:
        model = dept_master
        fields= '__all__'



#DESIGNATION SERIALIZER
class DesgSerializer(serializers.ModelSerializer):
    created_by = serializers.HiddenField(default=serializers.CurrentUserDefault())
    updated_by = serializers.HiddenField(default=serializers.CurrentUserDefault())
    # file = serializers.FileField(write_only=True)
    class Meta:
        model = desgntn_master
        fields= '__all__'

#DESIGNATION Bulk Upload SERIALIZER      
class DesgUploadSerializer(serializers.ModelSerializer):
    file = serializers.FileField(write_only=True)
    class Meta:
        model = desgntn_master
        fields= '__all__'


#CATOGARY SERIALIZER
class CtgrySerializer(serializers.ModelSerializer):
    created_by = serializers.HiddenField(default=serializers.CurrentUserDefault())
    updated_by = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = ctgry_master
        fields= '__all__'


class FiscalYearSerializer(serializers.ModelSerializer):
    class Meta:
        model = FiscalYear
        fields = '__all__'

class PeriodSerializer(serializers.ModelSerializer):
    class Meta:
        model = FiscalPeriod
        fields = '__all__'


#LANGUAGES
class LanguageMasterSerializer(serializers.ModelSerializer):
    # br_created_by = serializers.HiddenField(default=serializers.CurrentUserDefault())
    # br_updated_by = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model= LanguageMaster
        fields = '__all__'