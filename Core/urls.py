from django.urls import path, include
from .  views import (CountryViewSet,StateViewSet,CurrencyViewSet,CountryBulkuploadViewSet,DocumentTypeViewSet,
                      NationalityBlkupldViewSet)

from rest_framework.routers import DefaultRouter
router = DefaultRouter()

router.register(r'Country', CountryViewSet)
router.register(r'State', StateViewSet)
router.register(r'Bulkupload', CountryBulkuploadViewSet)
router.register(r'Nationality-Bulkupload', NationalityBlkupldViewSet)
router.register(r'Currency', CurrencyViewSet)
router.register(r'DocumentType', DocumentTypeViewSet)
urlpatterns = [
    # Other paths
    path('api/', include(router.urls)),

]