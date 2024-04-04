
# from rest_framework.permissions import BasePermission

# class CanExportDataPermission(BasePermission):
#     """
#     Custom permission to only allow users with specific permission to export data.
#     """

#     def has_permission(self, request, view):
#         # Check if the user has permission to export data
#         return request.user.has_perm('.export_data_permission')