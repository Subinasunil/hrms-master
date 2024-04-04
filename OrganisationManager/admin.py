# from django.contrib import admin
from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import cmpny_mastr,brnch_mstr,dept_master,desgntn_master
from .resource import BranchResource,DepartmentResource,DesignationResource


@admin.register(brnch_mstr)
class BranchAdmin(ImportExportModelAdmin):
    resource_class = BranchResource

@admin.register(dept_master)
class DepartmentAdmin(ImportExportModelAdmin):
    resource_class = DepartmentResource

@admin.register(desgntn_master)
class DesignationAdmin(ImportExportModelAdmin):
    resource_class = DesignationResource    

# Register your models here.
