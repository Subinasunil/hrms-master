from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status,generics,viewsets,permissions
from .models import (cmpny_mastr,brnch_mstr,LanguageMaster,dept_master,
                     desgntn_master,ctgry_master,FiscalPeriod,FiscalYear)
from . serializer import (CompanySerializer,BranchSerializer,LanguageMasterSerializer,
                          CtgrySerializer,DeptSerializer,DesgSerializer,FiscalYearSerializer,
                          PeriodSerializer,BranchuploadSerializer,DeptUploadSerializer,DesgUploadSerializer)
from rest_framework.decorators import action,api_view                         
from rest_framework.permissions import IsAuthenticated,AllowAny,IsAuthenticatedOrReadOnly,IsAdminUser
from UserManagement.permissions import IsAdminUser,IsSuperUser
from datetime import timedelta
from rest_framework.views import APIView

from rest_framework.parsers import MultiPartParser, FormParser
from .resource import (BranchResource,DepartmentResource,DesignationResource)
import pandas as pd
from tablib import Dataset



# Create your views here.
#COMPNY 
class CompanyViewSet(viewsets.ModelViewSet):
    queryset = cmpny_mastr.objects.all()
    serializer_class = CompanySerializer
    # authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        try:
            company_instance = serializer.save(cmpny_created_by=self.request.user)

            # Use get_or_create to check and create a branch if it doesn't exist
            branch_instance, created = brnch_mstr.objects.get_or_create(
                br_company_id=company_instance,
                defaults={
                    'branch_name': company_instance.cmpny_name,
                    'br_state_id': company_instance.cmpny_state_id,
                    'br_country': company_instance.cmpny_country,
                    'br_city': company_instance.cmpny_city,
                    'br_created_by': company_instance.cmpny_created_by,
                    'br_updated_by': company_instance.cmpny_updated_by,
                    'br_branch_mail': company_instance.cmpny_mail,
                    'br_branch_nmbr_1': company_instance.cmpny_nmbr_1,
                    # Add other fields as needed
                }
            )

            if not created:
                # Branch already existed, you can handle this case if needed
                pass

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    


    # def get_queryset(self):
    #     # Filter companies based on the currently authenticated user
    #     return cmpny_mastr.objects.filter(cmpny_created_by=self.request.user)
class BranchViewSet(viewsets.ModelViewSet):
    queryset = brnch_mstr.objects.all()
    serializer_class = BranchSerializer
    # authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    # def get_queryset(self):
    #     # Filter branches based on the currently authenticated user
    #     return brnch_mstr.objects.filter(br_created_by=self.request.user)

    def perform_create(self, serializer):
        # Set the user field to the currently authenticated user during creation
        serializer.save(br_created_by=self.request.user)  

#Branch Bulk Upload
class BranchUploadViewSet(viewsets.ModelViewSet):
    queryset = brnch_mstr.objects.all()
    serializer_class = BranchuploadSerializer
    # authentication_classes = [SessionAuthentication]
    # permission_classes = [IsAuthenticated]  

    @action(detail=False, methods=['post'])
    def bulk_upload(self, request):  
        if request.method == 'POST' and request.FILES.get('file'):
            excel_file = request.FILES['file']
            if excel_file.name.endswith('.xlsx'):
                try:
                    # Load data from the Excel file into a Dataset
                    dataset = Dataset()
                    dataset.load(excel_file.read(), format='xlsx')

                    # Create a resource instance
                    resource = BranchResource()

                    # Import data into the model using the resource
                    result = resource.import_data(dataset, dry_run=False, raise_errors=True)

                    return Response({"message": f"{result.total_rows} records created successfully"})
                except Exception as e:
                    return Response({"error": str(e)}, status=400)
            else:
                return Response({"error": "Invalid file format. Only Excel files (.xlsx) are supported."}, status=400)
        else:
            return Response({"error": "Please provide an Excel file."}, status=400)

    
#DEPARTMENT 
class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = dept_master.objects.all()
    serializer_class = DeptSerializer
    # authentication_classes = [SessionAuthentication,]
    
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        queryset = super().get_queryset()

        # Retrieve the branch_id from the query parameters
        branch_id = self.request.query_params.get('branch_id')

        # Filter departments based on the provided branch_id
        if branch_id:
            queryset = queryset.filter(branch_id=branch_id)
        return queryset 

 #Dept BulkUpload       
class DeptBulkUploadViewSet(viewsets.ModelViewSet):
    queryset = dept_master.objects.all()
    serializer_class = DeptUploadSerializer
    # authentication_classes = [SessionAuthentication,]
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['post'])
    def bulk_upload(self, request):
        if request.method == 'POST' and request.FILES.get('file'):
            excel_file = request.FILES['file']
            if excel_file.name.endswith('.xlsx'):
                try:
                    # Load data from the Excel file into a Dataset
                    dataset = Dataset()
                    dataset.load(excel_file.read(), format='xlsx')

                    # Create a resource instance
                    resource = DepartmentResource()

                    # Import data into the model using the resource
                    result = resource.import_data(dataset, dry_run=False, raise_errors=True)

                    return Response({"message": f"{result.total_rows} records created successfully"})
                except Exception as e:
                    return Response({"error": str(e)}, status=400)
            else:
                return Response({"error": "Invalid file format. Only Excel files (.xlsx) are supported."}, status=400)
        else:
            return Response({"error": "Please provide an Excel file."}, status=400)
    
#DESIGNATION 
class DesignationViewSet(viewsets.ModelViewSet):
    queryset = desgntn_master.objects.all()
    serializer_class = DesgSerializer
    # authentication_classes = [SessionAuthentication,]
    permission_classes = [IsAuthenticated,] 


#Designation BulkUpload
class DesignationBulkUploadViewSet(viewsets.ModelViewSet):
    queryset = desgntn_master.objects.all()
    serializer_class = DesgUploadSerializer
    # authentication_classes = [SessionAuthentication,]
    permission_classes = [IsAuthenticated,] 
    @action(detail=False, methods=['post'])
    def bulk_upload(self, request):
        if request.method == 'POST' and request.FILES.get('file'):
            excel_file = request.FILES['file']
            if excel_file.name.endswith('.xlsx'):
                try:
                    # Load data from the Excel file into a Dataset
                    dataset = Dataset()
                    dataset.load(excel_file.read(), format='xlsx')

                    # Create a resource instance
                    resource = DesignationResource()

                    # Import data into the model using the resource
                    result = resource.import_data(dataset, dry_run=False, raise_errors=True)

                    return Response({"message": f"{result.total_rows} records created successfully"})
                except Exception as e:
                    return Response({"error": str(e)}, status=400)
            else:
                return Response({"error": "Invalid file format. Only Excel files (.xlsx) are supported."}, status=400)
        else:
            return Response({"error": "Please provide an Excel file."}, status=400)
    
#CATOGARY CRUD
class CatogoryViewSet(viewsets.ModelViewSet):
    queryset = ctgry_master.objects.all()
    serializer_class = CtgrySerializer
    # authentication_classes = [SessionAuthentication,]
    permission_classes = [IsSuperUser,] 


class FiscalYearViewSet(viewsets.ModelViewSet):
    queryset = FiscalYear.objects.all()
    serializer_class = FiscalYearSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Create the FiscalYear instance
        self.perform_create(serializer)
        
        # Automatically create 12 FiscalPeriod instances with the same day next month
        fiscal_year = serializer.instance
        start_date = fiscal_year.start_date

        for period_number in range(1, 13):
            # Calculate the start and end dates of the period
            next_month_start_date = start_date.replace(day=1) + timedelta(days=32)  # Start of next month
            period_start_date = min(next_month_start_date, start_date.replace(day=start_date.day))
            period_end_date = (period_start_date.replace(day=1) + timedelta(days=31)).replace(day=start_date.day)

            FiscalPeriod.objects.create(
                fiscal_year=fiscal_year,
                period_number=period_number,
                start_date=period_start_date,
                end_date=period_end_date,
                company=fiscal_year.company_id
            )
            start_date = period_start_date  # Update start_date for the next iteration
        
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)



    # def create(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
        
    #     # Create the FiscalYear instance
    #     self.perform_create(serializer)
        
    #     # Automatically create 12 FiscalPeriod instances with a gap of 30 days
    #     fiscal_year = serializer.instance
    #     start_date = fiscal_year.start_date
    #     for period_number in range(1, 13):
    #         period_start_date = start_date + timedelta(days=(period_number - 1) * 30)
    #         period_end_date = period_start_date + timedelta(days=29)
    #         FiscalPeriod.objects.create(
    #             fiscal_year=fiscal_year,
    #             period_number=period_number,
    #             start_date=period_start_date,
    #             end_date=period_end_date,
    #             company=fiscal_year.company_id
    #         )
        
    #     headers = self.get_success_headers(serializer.data)
    #     return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class PeriodViewSet(viewsets.ModelViewSet):
    queryset = FiscalPeriod.objects.all()
    serializer_class = PeriodSerializer

class CompanyFiscalData(APIView):
    def get(self, request, company_id):
        try:
            fiscal_years = FiscalYear.objects.filter(company_id=company_id)
            fiscal_years_serializer = FiscalYearSerializer(fiscal_years, many=True)
            
            fiscal_periods = FiscalPeriod.objects.filter(company_id=company_id)
            fiscal_periods_serializer = PeriodSerializer(fiscal_periods, many=True)
            
            return Response({
                'fiscal_years': fiscal_years_serializer.data,
                'fiscal_periods': fiscal_periods_serializer.data
            })
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
        

class LanguageViewSet(viewsets.ModelViewSet):
    queryset = LanguageMaster.objects.all()
    serializer_class = LanguageMasterSerializer
    permission_classes = [IsAuthenticated]
    def get_serializer_context(self):
        return {'request': self.request}