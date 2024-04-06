from django.shortcuts import render
from django.contrib.auth.models import User,Group,Permission
from .serializers import RoleSerializer,CustomUserGroupSerializer,UserSerializer,PermissionSerializer
from . models import CustomUserGroup,CustomUser
from . permissions import (IsSuperAdminUser,IsSelfOrSuperAdmin,IsOwnerOrReadOnly,
                           IsOwnerOrHRAdminOrReadOnly,IsSuperUser,IsEssUserOrReadOnly)
from rest_framework.response import Response
from rest_framework import status,generics,viewsets,permissions
from rest_framework.permissions import IsAuthenticated,AllowAny,IsAuthenticatedOrReadOnly,IsAdminUser
from rest_framework.generics import ListAPIView
from rest_framework.decorators import action
from django.contrib.auth.hashers import make_password
from EmpManagement.serializer import Emp_qf_Serializer,EmpFamSerializer,EmpJobHistorySerializer,EmpLeaveRequestSerializer,DocumentSerializer
# Create your views here.
#usergroups or roles

class RegisterUserAPIView(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    # permission_classes = [IsSuperAdminUser]
   
    def get_serializer_context(self):
        return {'request': self.request}

class PermissionViewSet(viewsets.ModelViewSet):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer


class UserRolesViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [IsSuperUser]


# # user grouping with permissions

class UserandPermissionGrouping(viewsets.ModelViewSet):
    queryset = CustomUserGroup.objects.all()
    serializer_class = CustomUserGroupSerializer
    permission_classes = [IsSuperUser]
    

