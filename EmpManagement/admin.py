
# from django.contrib import admin
from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import emp_master
from .resource import EmployeeResource

@admin.register(emp_master)
class EmployeeAdmin(ImportExportModelAdmin):
    resource_class = EmployeeResource
# Register your models here.
