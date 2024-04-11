from django.conf import settings
from django.shortcuts import render
from .models import (emp_family,Emp_Documents,EmpJobHistory,EmpLeaveRequest,EmpQualification,
                     emp_master,Emp_CustomField,EmpFamily_CustomField,EmpJobHistory_CustomField,
                     EmpQualification_CustomField,EmpDocuments_CustomField)
from .serializer import (Emp_qf_Serializer,EmpFamSerializer,EmpSerializer,
                         EmpJobHistorySerializer,EmpLeaveRequestSerializer,DocumentSerializer,EmpBulkUploadSerializer,CustomFieldSerializer,
                         EmpFam_CustomFieldSerializer,EmpJobHistory_Udf_Serializer,Emp_qf_udf_Serializer,EmpDocuments_Udf_Serializer)
from rest_framework.decorators import action,api_view
from rest_framework import viewsets,filters,parsers
from rest_framework.response import Response
from rest_framework import status,generics,viewsets,permissions
# from rest_framework.authentication import SessionAuthentication,TokenAuthentication
from rest_framework.permissions import IsAuthenticated,AllowAny,IsAuthenticatedOrReadOnly,IsAdminUser
# from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
# from rest_framework.decorators import api_view
# from rest_framework.response import Response
from django.http import FileResponse,HttpResponse
from openpyxl import Workbook
from rest_framework.parsers import MultiPartParser, FormParser
from .resource import EmployeeResource,EmpResource_Export,EmpCustomFieldResource
import tablib
import pandas as pd
import openpyxl
import xlsxwriter
import io
import os
from django.db import transaction
from django.core.exceptions import ValidationError
from import_export.results import RowResult
from tablib import Dataset
from io import BytesIO
from rest_framework.permissions import IsAuthenticated
# from .permissions import CanExportDataPermission
from rest_framework.permissions import IsAdminUser
from django.contrib.auth.decorators import permission_required
from openpyxl.utils import get_column_letter
from openpyxl import Workbook
from openpyxl.styles import PatternFill,Alignment
from django.core.files import File 

from django.http import HttpResponse
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter,landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib.units import inch
import requests
import json

# from django. utils. timezone import timedelta
# from django.utils import timezone
# from UserManagement.models import CustomUser
# Create your views here.
#EMPLOYEE CRUD
class EmpViewSet(viewsets.ModelViewSet):
    queryset = emp_master.objects.all()
    serializer_class = EmpSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)

   


    @action(detail=True, methods=['get'])
    def emp_family(self, request, pk=None):
        employee = self.get_object()
        families = employee.emp_family.all()  
        serializer = EmpFamSerializer(families, many=True)
        return Response(serializer.data)
    @action(detail=True, methods=['get'])
    def emp_qualification(self, request, pk=None):
        employee = self.get_object()
        qualification = employee.emp_qualification.all()  
        serializer = Emp_qf_Serializer(qualification, many=True)
        return Response(serializer.data)
    @action(detail=True, methods=['get'])
    def emp_job_history(self, request, pk=None):
        employee = self.get_object()
        job_history = employee.emp_job_history.all()  
        serializer = EmpJobHistorySerializer(job_history, many=True)
        return Response(serializer.data)
    @action(detail=True, methods=['get'])
    def emp_documents(self, request, pk=None):
        employee = self.get_object()
        Emp_Documents = employee.emp_documents.all()  
        serializer = DocumentSerializer(Emp_Documents, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def emp_udf(self, request, pk=None):
        udf = self.get_object()
        userdefinedfields = udf.custom_fields.all()  
        serializer = CustomFieldSerializer(userdefinedfields, many=True)
        return Response(serializer.data)


    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            if user.is_ess:  # If user is an ESS, they can only access their own employee information
                return emp_master.objects.filter(created_by=user)
            else:
                return emp_master.objects.all()  # Other users can access all employee information
    
        return emp_master.objects.none()  # Return an empty queryset for unauthenticated users

    


    @action(detail=False, methods=['get'],permission_classes=[IsAdminUser])
    def export_employee_data(self, request):
        if not request.user.is_superuser:
            return Response({"error": "You do not have permission to access this resource."}, status=status.HTTP_403_FORBIDDEN)
        queryset = emp_master.objects.all()
        resource = EmpResource_Export()
        dataset = resource.export(queryset)

        # Create an Excel workbook
        wb = Workbook()
        ws = wb.active

        # Define default cell formats
        default_fill = PatternFill(start_color='FFC0CB', end_color='FFC0CB', fill_type='solid')  # pink background color
        default_alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)

        # Apply default styles to headings
        for col_num, field_name in enumerate(dataset.headers):
            ws.cell(row=1, column=col_num + 1, value=field_name)
            ws.cell(row=1, column=col_num + 1).fill = default_fill
            ws.cell(row=1, column=col_num + 1).alignment = default_alignment

        # Write data to the Excel file
        for row_num, row in enumerate(dataset, start=2):
            for col_num, value in enumerate(row, start=1):
                ws.cell(row=row_num, column=col_num, value=value)
                ws.cell(row=row_num, column=col_num).alignment = default_alignment

        # Auto-size columns
        for col in ws.columns:
            max_length = 0
            for cell in col:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(str(cell.value))
                except:
                    pass
            adjusted_width = (max_length + 2) * 1.2
            ws.column_dimensions[col[0].column_letter].width = adjusted_width

        # Save the workbook to an in-memory buffer
        buffer = BytesIO()
        wb.save(buffer)
        buffer.seek(0)

        # Prepare response
        response = HttpResponse(buffer.getvalue(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="exported_data.xlsx"'
        return response

    @action(detail=False, methods=['get'])
    def emp_pdf_report(self, request, *args, **kwargs):
        # Query employee details from the database
        employees = emp_master.objects.all()

        # Create a response object
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="employee_report.pdf"'

        # Create a PDF document
        pdf = SimpleDocTemplate(response, pagesize=letter)
        
        # Create a table to hold employee details
        data = [["ID", "FirstName", "LastName", "Gender", "DOB", "Email", "Mobile Number", "Country", "State", "City", "Permanent Address", "Present Address", "Status", "Hired Date", "Religion", "Blood Group", "Nationality", "Marital Status", "Father Name", "Mother Name", "Posting Location","Created At", "Created By", "Updated At", "Updated By","Active","OT Applicable", "Company", "Branch", "Department", "Designation", "Category"]]
        
        for employee in employees:
            data.append([
                employee.emp_login_id,
                employee.emp_first_name,
                employee.emp_last_name,
                employee.get_emp_gender_display() if employee.emp_gender else "",  # Get display value for choices field
                employee.emp_date_of_birth,
                employee.emp_personal_email,
                employee.emp_mobile_number_1,
                employee.emp_country_id.country_name if employee.emp_country_id else "",  # Assuming 'name' is the field for country name
                employee.emp_state_id.state_name if employee.emp_state_id else "",  # Assuming 'name' is the field for state name
                employee.emp_city,
                employee.emp_permenent_address,
                employee.emp_present_address,
                "Active" if employee.emp_status else "Inactive",
                employee.emp_hired_date,
                employee.emp_relegion,
                employee.emp_blood_group,
                employee.emp_nationality,
                employee.get_emp_marital_status_display() if employee.emp_marital_status else "",  # Get display value for choices field
                employee.emp_father_name,
                employee.emp_mother_name,
                employee.emp_posting_location,
                employee.created_at,
                employee.created_by.username if employee.created_by else "",  # Assuming 'username' is the field for username
                employee.updated_at,
                employee.updated_by.username if employee.updated_by else "",  # Assuming 'username' is the field for username
                "Active" if employee.is_active else "Inactive",
                "Yes" if employee.epm_ot_applicable else "No",
                employee.emp_company_id.cmpny_name if employee.emp_company_id else "",  # Assuming 'name' is the field for company name
                employee.emp_branch_id.branch_name if employee.emp_branch_id else "",  # Assuming 'name' is the field for branch name
                employee.emp_dept_id.dept_name if employee.emp_dept_id else "",  # Assuming 'name' is the field for department name
                employee.emp_desgntn_id.job_title if employee.emp_desgntn_id else "",  # Assuming 'name' is the field for designation name
                employee.emp_ctgry_id.catogary_title if employee.emp_ctgry_id else "",  # Assuming 'name' is the field for category name
            ])

        
        # Calculate column widths based on content
        col_widths = [1 * inch] * len(data[0])  # Initialize with default width (1.2 inch per column)
        for row in data:
            for i, cell in enumerate(row):
                col_widths[i] = max(col_widths[i], len(str(cell)) * 0.10 * inch)  # Adjust width based on content length

        # Calculate total table width
        total_width = sum(col_widths)

        # Set page size to accommodate the table width
        pdf.pagesize = (total_width, letter[1])  # Use the total width calculated and keep the height same as letter page height



       # Create the table with adjusted column widths and enable text wrapping
        table = Table(data, colWidths=col_widths, repeatRows=1)
        table.setStyle(TableStyle([('WORDWRAP', (0, 0), (-1, -1), True)]))

        # Add style to the table
        style = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.gray),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),  # Vertical alignment
                    ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),  # Text color
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),  # Header text color
                    ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),  # Font
                    ('FONT_SIZE', (0, 0), (-1, -1), 10),  # Font size
                    ('WORD_WRAP', (0, 0), (-1, -1), True)])  # Enable word wrap

        table.setStyle(style)

        # Add the table to the PDF document
        elements = [table]
        pdf.build(elements)

        return response
class CustomFieldViewset(viewsets.ModelViewSet):
    queryset = Emp_CustomField.objects.all()
    serializer_class = CustomFieldSerializer
    permission_classes = [IsAuthenticated]

    def handle_exception(self, exc):
        if isinstance(exc, ValidationError):
            error_messages = [str(error) for error in exc]
            error_message = ', '.join(error_messages)
            return Response({'error': error_message}, status=status.HTTP_400_BAD_REQUEST)
        
        return super().handle_exception(exc)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        data_type = serializer.validated_data.get('data_type')
        if not data_type:
            return Response({'error': 'Please select a data type.'}, status=status.HTTP_400_BAD_REQUEST)
        
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class EmpFam_CustomFieldViewset(viewsets.ModelViewSet):
    queryset = EmpFamily_CustomField.objects.all()
    serializer_class = EmpFam_CustomFieldSerializer
    permission_classes = [IsAuthenticated]

    def handle_exception(self, exc):
        if isinstance(exc, ValidationError):
            error_messages = [str(error) for error in exc]
            error_message = ', '.join(error_messages)
            return Response({'error': error_message}, status=status.HTTP_400_BAD_REQUEST)
        
        return super().handle_exception(exc)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        data_type = serializer.validated_data.get('data_type')
        if not data_type:
            return Response({'error': 'Please select a data type.'}, status=status.HTTP_400_BAD_REQUEST)
        
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class EmpJobHistory_UdfViewset(viewsets.ModelViewSet):
    queryset = EmpJobHistory_CustomField.objects.all()
    serializer_class = EmpJobHistory_Udf_Serializer
    permission_classes = [IsAuthenticated]

    def handle_exception(self, exc):
        if isinstance(exc, ValidationError):
            error_messages = [str(error) for error in exc]
            error_message = ', '.join(error_messages)
            return Response({'error': error_message}, status=status.HTTP_400_BAD_REQUEST)
        
        return super().handle_exception(exc)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        data_type = serializer.validated_data.get('data_type')
        if not data_type:
            return Response({'error': 'Please select a data type.'}, status=status.HTTP_400_BAD_REQUEST)
        
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class EmpQf_UdfViewset(viewsets.ModelViewSet):
    queryset = EmpQualification_CustomField.objects.all()
    serializer_class = Emp_qf_udf_Serializer
    permission_classes = [IsAuthenticated]

    def handle_exception(self, exc):
        if isinstance(exc, ValidationError):
            error_messages = [str(error) for error in exc]
            error_message = ', '.join(error_messages)
            return Response({'error': error_message}, status=status.HTTP_400_BAD_REQUEST)
        
        return super().handle_exception(exc)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        data_type = serializer.validated_data.get('data_type')
        if not data_type:
            return Response({'error': 'Please select a data type.'}, status=status.HTTP_400_BAD_REQUEST)
        
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class EmpDoc_UdfViewset(viewsets.ModelViewSet):
    queryset = EmpDocuments_CustomField.objects.all()
    serializer_class = EmpDocuments_Udf_Serializer
    permission_classes = [IsAuthenticated]

    def handle_exception(self, exc):
        if isinstance(exc, ValidationError):
            error_messages = [str(error) for error in exc]
            error_message = ', '.join(error_messages)
            return Response({'error': error_message}, status=status.HTTP_400_BAD_REQUEST)
        
        return super().handle_exception(exc)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        data_type = serializer.validated_data.get('data_type')
        if not data_type:
            return Response({'error': 'Please select a data type.'}, status=status.HTTP_400_BAD_REQUEST)
        
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


#emp bulkupload

class EmpbulkuploadViewSet(viewsets.ModelViewSet):
    queryset = emp_master.objects.all()
    serializer_class = EmpBulkUploadSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)

    # @action(detail=False, methods=['post'], parser_classes=[MultiPartParser, FormParser])
    # def bulk_upload(self, request):
    #     if request.method == 'POST' and request.FILES.get('file'):
    #         excel_file = request.FILES['file']
    #         if excel_file.name.endswith('.xlsx'):
    #             try:
    #                 # Load data from the Excel file into a Dataset
    #                 dataset = Dataset()
    #                 dataset.load(excel_file.read(), format='xlsx')

    #                 # Create resource instances for Employee and CustomField
    #                 employee_resource = EmployeeResource()
    #                 custom_field_resource = EmpCustomFieldResource()

    #                 # Collect errors for Employee resource
    #                 employee_errors = []
    #                 with transaction.atomic():
    #                     for row_idx, row in enumerate(dataset.dict, start=2):  # Start from row 2 (1-based index)
    #                         try:
    #                             employee_resource.before_import_row(row, row_idx=row_idx)
    #                         except ValidationError as e:
    #                             employee_errors.extend([f"Row {row_idx}: {error}" for error in e.messages])

    #                 # Collect errors for CustomField resource
    #                 custom_field_errors = []
    #                 with transaction.atomic():
    #                     for row_idx, row in enumerate(dataset.dict, start=2):  # Start from row 2 (1-based index)
    #                         try:
    #                             custom_field_resource.before_import_row(row, row_idx=row_idx)
    #                         except ValidationError as e:
    #                             custom_field_errors.extend([f"Row {row_idx}: {error}" for error in e.messages])

    #                 # Merge errors from both resources
    #                 all_errors = employee_errors + custom_field_errors

    #                 # If there are any errors, return them
    #                 if all_errors:
    #                     return Response({"errors": all_errors}, status=400)

    #                 # If no errors, import valid data into the models
    #                 with transaction.atomic():
    #                     employee_result = employee_resource.import_data(dataset, dry_run=False, raise_errors=True)
    #                     custom_field_result = custom_field_resource.import_data(dataset, dry_run=False, raise_errors=True)

    #                 return Response({"message": f"{employee_result.total_rows} records created successfully"})
    #             except Exception as e:
    #                 return Response({"error": str(e)}, status=400)
    #         else:
    #             return Response({"error": "Invalid file format. Only Excel files (.xlsx) are supported."}, status=400)
    #     else:
    #         return Response({"error": "Please provide an Excel file."}, status=400)


    @action(detail=False, methods=['post'], parser_classes=[MultiPartParser, FormParser])
    def bulk_upload(self, request):
        if request.method == 'POST' and request.FILES.get('file'):
            excel_file = request.FILES['file']
            if excel_file.name.endswith('.xlsx'):
                try:
                    # Open the Excel file
                    workbook = openpyxl.load_workbook(excel_file)

                    # Initialize error lists
                    all_errors_sheet1 = []
                    all_errors_sheet2 = []

                    # Extract data from each sheet if it exists and is not empty
                    sheet1 = workbook.get_sheet_by_name('Sheet1')
                    sheet2 = workbook.get_sheet_by_name('Sheet2')

                    if sheet1 is None or sheet1.max_row == 1:
                        return Response({"error": "Sheet1 is either missing or empty."}, status=400)

                    if sheet2 is None or sheet2.max_row == 1:
                        return Response({"error": "Sheet2 is either missing or empty."}, status=400)

                    # Convert data to datasets
                    dataset_sheet1 = Dataset()
                    dataset_sheet1.headers = [cell.value for cell in sheet1[1]]
                    for row_idx, row in enumerate(sheet1.iter_rows(min_row=2), start=2):
                        dataset_sheet1.append([cell.value for cell in row])

                    dataset_sheet2 = Dataset()
                    dataset_sheet2.headers = [cell.value for cell in sheet2[1]]
                    for row_idx, row in enumerate(sheet2.iter_rows(min_row=2), start=2):
                        dataset_sheet2.append([str(cell.value) for cell in row])

                    # Create resource instances for Employee and CustomField
                    employee_resource = EmployeeResource()
                    custom_field_resource = EmpCustomFieldResource()

                    # Validate and collect errors from Sheet1
                    with transaction.atomic():
                        for row_idx, row in enumerate(dataset_sheet1.dict, start=2):
                            try:
                                employee_resource.before_import_row(row, row_idx=row_idx)
                            except Exception as e:
                                all_errors_sheet1.append({"row": row_idx, "error": str(e)})

                    # Validate and collect errors from Sheet2
                    with transaction.atomic():
                        for row_idx, row in enumerate(dataset_sheet2.dict, start=2):
                            try:
                                custom_field_resource.before_import_row(row, row_idx=row_idx)
                            except Exception as e:
                                all_errors_sheet2.append({"row": row_idx, "error": str(e)})

                    # Check if there are any errors and return them
                    if all_errors_sheet1 or all_errors_sheet2:
                        return Response({"errors_sheet1": all_errors_sheet1, "errors_sheet2": all_errors_sheet2}, status=400)

                    # If no errors, proceed with importing data

                    # Import data from Sheet1 into emp_master table
                    with transaction.atomic():
                        employee_result = employee_resource.import_data(dataset_sheet1, dry_run=False, raise_errors=True)

                    # Import data from Sheet2 into Emp_CustomField table
                    with transaction.atomic():
                        custom_field_result = custom_field_resource.import_data(dataset_sheet2, dry_run=False, raise_errors=True)

                    return Response({"message": f"{employee_result.total_rows} records created for Sheet1, {custom_field_result.total_rows} records created for Sheet2 successfully"})
                except Exception as e:
                    return Response({"error": str(e)}, status=400)
            else:
                return Response({"error": "Invalid file format. Only Excel files (.xlsx) are supported."}, status=400)
        else:
            return Response({"error": "Please provide an Excel file."}, status=400)
            

    @action(detail=False, methods=['get'])  # New endpoint for downloading default file
    def download_default_excel_file(self, request):
        # demo_file_path = os.path.join(settings.BASE_DIR,'defaults', 'emp mstr.xlsx')
        demo_file_path = os.path.join(os.path.dirname(__file__), 'defaults', 'emp mstr.xlsx')
        try:
            with open(demo_file_path, 'rb') as f:
                response = HttpResponse(f.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
                response['Content-Disposition'] = 'attachment; filename="demo.xlsx"'
                return response
        except FileNotFoundError:
            return Response({"error": "Default demo file not found."}, status=400)

#EMP_FAMILY
class EmpFamViewSet(viewsets.ModelViewSet):
    queryset = emp_family.objects.all()  # Retrieve all instances of emp_family model
    serializer_class = EmpFamSerializer  # Use EmpFamSerializer for serialization
    permission_classes = [IsAuthenticated]  # Require authentication for access

    @action(detail=True, methods=['get'])
    def empfamily_udf(self, request, pk=None):
        fam_udf = self.get_object()
        userdefinedfields = fam_udf.custom_fields.all()  
        serializer = EmpFam_CustomFieldSerializer(userdefinedfields, many=True)
        return Response(serializer.data)

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:  # Check if user is authenticated
            if user.is_superuser or user.is_staff:  # Check if user is a superuser or staff
                return emp_family.objects.all()  # Return all instances of emp_family
            elif hasattr(user, 'emp_id'):  # If not a superuser or staff, filter based on emp_id
                return emp_family.objects.filter(emp_id=user.emp_id)
            elif user.is_ess:  # If user is an ESS, filter based on created_by
                return emp_family.objects.filter(created_by=user)
        return emp_family.objects.none()  # Return an empty queryset if user is not authenticated or does not meet any condition

#EMP_JOB HISTORY
#EMP_JOB HISTORY
class EmpJobHistoryvSet(viewsets.ModelViewSet):
    queryset = EmpJobHistory.objects.all()
    serializer_class = EmpJobHistorySerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['get'])
    def empjobhistory_udf(self, request, pk=None):
        jobhistory_udf = self.get_object()
        userdefinedfields = jobhistory_udf.custom_fields.all()  
        serializer = EmpJobHistory_Udf_Serializer(userdefinedfields, many=True)
        return Response(serializer.data)

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            if user.is_superuser or user.is_staff:  # Check if user is a superuser or staff
                return EmpJobHistory.objects.all()  # Return all instances of emp_family
            elif hasattr(user, 'emp_id'):  # Assuming 'emp_id' is the attribute that stores employee ID
                return EmpJobHistory.objects.filter(emp_id=user.emp_id)
            elif user.is_ess:  # If user is an ESS, filter based on created_by
                return EmpJobHistory.objects.filter(created_by=user)
        return EmpJobHistory.objects.none()
    def get_serializer_context(self):
        return {'request': self.request}
    
#EMP_QUALIFICATION HISTORY


class Emp_QualificationViewSet(viewsets.ModelViewSet):
    queryset = EmpQualification.objects.all()
    serializer_class = Emp_qf_Serializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['get'])
    def empqualification_udf(self, request, pk=None):
        emp_qf_udf = self.get_object()
        userdefinedfields = emp_qf_udf.custom_fields.all()  
        serializer = Emp_qf_Serializer(userdefinedfields, many=True)
        return Response(serializer.data)

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            if user.is_superuser or user.is_staff:  # Check if user is a superuser or staff
                return EmpQualification.objects.all()  # Return all instances of emp_family
            elif hasattr(user, 'emp_id'):  # Assuming 'emp_id' is the attribute that stores employee ID
                return EmpQualification.objects.filter(emp_id=user.emp_id)
            elif user.is_ess:  # If user is an ESS, filter based on created_by
                return EmpQualification.objects.filter(created_by=user)
        return EmpQualification.objects.none()
    def get_serializer_context(self):
        return {'request': self.request}
    

#EMP_DOCUMENT 



class Emp_DocumentViewSet(viewsets.ModelViewSet):
    queryset = Emp_Documents.objects.all()
    serializer_class = DocumentSerializer
    permission_classes = [IsAuthenticated]
    
    @action(detail=True, methods=['get'])
    def empfamily_udf(self, request, pk=None):
        empDoc_udf = self.get_object()
        userdefinedfields = empDoc_udf.custom_fields.all()  
        serializer = EmpDocuments_Udf_Serializer(userdefinedfields, many=True)
        return Response(serializer.data)
    
    
    def get_serializer_context(self):
        return {'request': self.request}
    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            if user.is_superuser or user.is_staff:  # Check if user is a superuser or staff
                return Emp_Documents.objects.all()  # Return all instances of emp_family
            elif hasattr(user, 'emp_id'):  # Assuming 'emp_id' is the attribute that stores employee ID
                return Emp_Documents.objects.filter(emp_id=user.emp_id)
            elif user.is_ess:  # If user is an ESS, filter based on created_by
                return Emp_Documents.objects.filter(created_by=user)
        return Emp_Documents.objects.none()
        # if user.emp_doc_expiry_date - date.today().days <= 7

    
    



# EmpLeaveRequest
class EmpLeaveRequestViewSet(viewsets.ModelViewSet):
    queryset = EmpLeaveRequest.objects.all()
    serializer_class = EmpLeaveRequestSerializer
    permission_classes = [IsAuthenticated]
    def get_serializer_context(self):
        return {'request': self.request}