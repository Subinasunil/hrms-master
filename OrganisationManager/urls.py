from django.urls import path, include
from . views import (FiscalYearViewSet,PeriodViewSet,CompanyViewSet,BranchViewSet,DepartmentViewSet,
                     DesignationViewSet,CatogoryViewSet,LanguageViewSet,CompanyFiscalData,
                     BranchUploadViewSet,DeptBulkUploadViewSet,DesignationBulkUploadViewSet)
from rest_framework.routers import DefaultRouter

router = DefaultRouter()


router.register(r'Company', CompanyViewSet)
router.register(r'Branch', BranchViewSet)
router.register(r'B-BulkUpload', BranchUploadViewSet,basename='emp-bulkupload')
router.register(r'Department', DepartmentViewSet)
router.register(r'Dept-BulkUpload', DeptBulkUploadViewSet,basename='dept-bulkupload')
router.register(r'Designation', DesignationViewSet)
router.register(r'Designtn-BulkUpload', DesignationBulkUploadViewSet,basename='designtn-bulkupload')
router.register(r'Catogory', CatogoryViewSet)
router.register(r'fiscal-years', FiscalYearViewSet)
router.register(r'periods', PeriodViewSet)
router.register(r'emp-Language', LanguageViewSet)


urlpatterns = [
    # Other paths
    path('api/', include(router.urls)),

    path('company-fiscal-data/<int:company_id>/', CompanyFiscalData.as_view(), name='company-fiscal-data'),
    # path('api/Branch/bulk-upload/', BranchViewSet.as_view({'post': 'bulk_upload'}), name='bulk-upload'),
    # path('api/Department/bulk-upload/', DepartmentViewSet.as_view({'post': 'bulk_upload'}), name='bulk-upload'),
    # path('api/Designation/bulk-upload/', DesignationViewSet.as_view({'post': 'bulk_upload'}), name='bulk-upload'),
    # path('profile_pic/<str:filename>/', profile_pic_view, name='profile_pic'),
    # path('countries/<int:pk>/', StateByCountryAPIView.as_view(), name='states-by-country'),

]