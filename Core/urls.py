from django.urls import path, include
from .  views import (CountryViewSet,StateViewSet,CurrencyViewSet)

from rest_framework.routers import DefaultRouter
router = DefaultRouter()

router.register(r'Country', CountryViewSet)
router.register(r'State', StateViewSet)

router.register(r'Currency', CurrencyViewSet)
urlpatterns = [
    # Other paths
    path('api/', include(router.urls)),

]