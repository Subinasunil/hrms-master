from import_export import resources
from import_export.admin import ImportMixin
from import_export.signals import post_import
from import_export.fields import Field
from .models import cmpny_mastr,brnch_mstr,dept_master,desgntn_master

class BranchResource(resources.ModelResource):
    class Meta:
        model = brnch_mstr
       
        fields = ('id',
                  'branch_name',
                  'br_company_id',
                  'br_is_active',
                  'br_state_id',
                  'br_city',
                  'br_pincode',
                  'br_branch_nmbr_1',
                  'br_branch_nmbr_2',
                  'br_branch_mail',
                  'br_country',
                  'br_created_at',
                  'br_created_by',
                  'br_updated_at',
                  'br_updated_by',     
                                       
        )
class DepartmentResource(resources.ModelResource):
    class Meta:
        model = dept_master
       
        fields = ('id',
                  'dept_name',
                  'description',
                  'created_at',
                  'created_by',
                  'updated_at',
                  'updated_by',
                  'is_active',
                  'branch_id',  
        ) 
class DesignationResource(resources.ModelResource):
    class Meta:
        model = desgntn_master
       
        fields = ('id',
                  'job_title',
                  'description',
                  'created_at',
                  'created_by',
                  'updated_at',
                  'updated_by',
                  'is_active',
        )             




        