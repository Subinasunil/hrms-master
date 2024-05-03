from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (EmpFamViewSet, EmpJobHistoryvSet, EmpViewSet,
                    Emp_QualificationViewSet, Emp_DocumentViewSet, EmpLeaveRequestViewSet,EmpbulkuploadViewSet,
                    CustomFieldViewset,EmpFam_CustomFieldViewset,EmpJobHistory_UdfViewset,EmpQf_UdfViewset,EmpDoc_UdfViewset,
                    Bulkupload_DocumentViewSet,LanguageSkillViewSet,MarketingSkillViewSet,ProgrammingLanguageSkillViewSet,EmployeeSkillViewSet,
                    LanguageBlkupldViewSet,ProLangBlkupldViewSet,MarketingBlkupldViewSet,GenerateEmployeeExcelReport,
                    )
                   

# Define the main router for top-level routes
router = DefaultRouter()
router.register(r'Employee', EmpViewSet, basename='employee')
router.register(r'emp-BulkUpload', EmpbulkuploadViewSet, basename='emp_bulk_upload')
router.register(r'custom-field', CustomFieldViewset, basename='custom-field')
router.register(r'emp-Family', EmpFamViewSet, basename='emp_family')
router.register(r'empfamily-UDF', EmpFam_CustomFieldViewset, basename='emp_fam_udf')
router.register(r'emp-JobHistory', EmpJobHistoryvSet, basename='emp_job_history')
router.register(r'empjob-history-UDF', EmpJobHistory_UdfViewset, basename='emp_job_history_udf')
router.register(r'emp-Qualification', Emp_QualificationViewSet, basename='emp_qualification')
router.register(r'empQualification-UDF', EmpQf_UdfViewset, basename='emp_qualification_udf')
router.register(r'emp-Documents', Emp_DocumentViewSet, basename='emp_document')
router.register(r'Bulkupload-Documents', Bulkupload_DocumentViewSet, basename='bulk_upload_document')
router.register(r'emp-Documents-UDF', EmpDoc_UdfViewset, basename='emp_document_udf')
router.register(r'emp-leave-request', EmpLeaveRequestViewSet)
router.register(r'emp-language-skill',LanguageSkillViewSet, basename='emp_language_skill')
router.register(r'emp-marketing-skill',MarketingSkillViewSet, basename='emp_marketing_skill')
router.register(r'emp-programing-language-skill',ProgrammingLanguageSkillViewSet, basename='emp_programming_language_skill')
router.register(r'emp-skill',EmployeeSkillViewSet, basename='emp_skill')
# router.register(r'emp-skill', SkillMasterViewSet, basename='emp_skill')
router.register(r'emp-language-skill-blkupld', LanguageBlkupldViewSet, basename='emp_language_skillblkupld')
router.register(r'emp-marketing-skill-blkupld', MarketingBlkupldViewSet, basename='emp_marketing_skillblkupld')
router.register(r'emp-programming-skill-blkupld', ProLangBlkupldViewSet, basename='emp_programming_skillblkupld')


# Define nested routes for accessing related resources under each employee

employee_router = DefaultRouter()
employee_router.register(r'emp-bulkupload', EmpbulkuploadViewSet, basename='emp-bulkupload')
employee_router.register(r'emp-family', EmpFamViewSet, basename='employee-family')
employee_router.register(r'emp-jobhistory', EmpJobHistoryvSet, basename='employee-jobhistory')
employee_router.register(r'emp-qualification', Emp_QualificationViewSet, basename='employee-qualification')
employee_router.register(r'emp-documents', Emp_DocumentViewSet, basename='employee-documents')
employee_router.register(r'emp-leave-request', EmpLeaveRequestViewSet, basename='employee-leave-request')

# Define the URL patterns
urlpatterns = [
    path('api/', include(router.urls)),
    path('api/Employee/<int:pk>/', include(employee_router.urls)),  # Nested routes for individual employees
    path('emp-documents/check-expiry-alert/', Emp_DocumentViewSet.as_view({'get': 'check_expiry_alert'}), name='check-expiry-alert'),
    path('api/Employee/bulk-upload/', EmpViewSet.as_view({'post': 'bulk_upload'}), name='bulk-upload'),
    path('api/Employee/emp_pdf_report/', EmpViewSet.as_view({'get': 'emp_pdf_report'}), name='emp_pdf_report'),
    path('api/Employee/<int:pk>/add_custom_field/', EmpViewSet.as_view({'patch': 'add_field'}), name='add_custom_field'),
    path('employee/api/Employee/select_fields/', EmpViewSet.as_view({'get': 'select_fields'}), name='select_fields'),
    path('employee/api/Employee/emp_select_report/', EmpViewSet.as_view({'post': 'emp_select_report'}), name='emp_select_report'),
    path('generate-report/', GenerateEmployeeExcelReport.as_view(), name='generate_employee_excel_report'),
    
]