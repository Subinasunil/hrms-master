from django.shortcuts import render
from django.contrib import messages
from .models import (state_mstr,crncy_mstr,cntry_mstr)
from .serializer import (CountrySerializer,StateSerializer,CurrencySerializer)
from rest_framework.decorators import action
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status,generics,viewsets,permissions
from rest_framework.authentication import SessionAuthentication,TokenAuthentication
from rest_framework.permissions import IsAuthenticated,AllowAny,IsAuthenticatedOrReadOnly,IsAdminUser

# Create your views here.

#STATE CRUD
class StateViewSet(viewsets.ModelViewSet):
    queryset = state_mstr.objects.all()
    serializer_class = StateSerializer
    # authentication_classes = [SessionAuthentication,]
    permission_classes = [IsAdminUser,] 

    # def list(self, request):
    #     country_id = request.query_params.get('country_id')
    #     if country_id:
    #         states = self.queryset.filter(country_id=country_id)
    #         serializer = self.serializer_class(states, many=True)
    #         return Response(serializer.data)
    #     else:
    #         return Response({"error": "Country ID is required"})
#COUNTRY CRUD
class CountryViewSet(viewsets.ModelViewSet):
    queryset = cntry_mstr.objects.all()
    serializer_class = CountrySerializer
    # authentication_classes = [SessionAuthentication,]
    permission_classes = [IsAdminUser,]

    # Custom action to get states for a specific country
    @action(detail=True, methods=['get'])
    def states(self, request, pk=None):
        country = self.get_object()
        states = country.state_mstr_set.all()  # Use the correct related_name
        serializer = StateSerializer(states, many=True)
        return Response(serializer.data)

        

#CURRENCY CRUD+
class CurrencyViewSet(viewsets.ModelViewSet):
    queryset = crncy_mstr.objects.all()
    serializer_class = CurrencySerializer
    # authentication_classes = [SessionAuthentication,]
    permission_classes = [IsAdminUser,] 
    


