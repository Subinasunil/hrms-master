from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.views import TokenObtainPairView

from .views import RegisterUserAPIView,UserRolesViewSet,UserandPermissionGrouping,PermissionViewSet


router = DefaultRouter()

router.register(r'user', RegisterUserAPIView)
router.register(r'Role-Grouping', UserRolesViewSet)
router.register(r'permissions', PermissionViewSet)
router.register(r'UserandPermissionGrouping', UserandPermissionGrouping)


urlpatterns = [
    # Other paths
    path('api/', include(router.urls)),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('api/userregister/',RegisterUserAPIView.as_view()),
    # path('api/userlist/', UserListView.as_view(), ),
    # path('company-fiscal-data/<int:company_id>/', CompanyFiscalData.as_view(), name='company-fiscal-data'),
    # path('profile_pic/<str:filename>/', profile_pic_view, name='profile_pic'),
    # path('countries/<int:pk>/', StateByCountryAPIView.as_view(), name='states-by-country'),

]