from django.contrib.auth.models import Group,Permission
from rest_framework import serializers
from .models import CustomUser, CustomUserGroup
from OrganisationManager.models import cmpny_mastr, brnch_mstr
from OrganisationManager.serializer import BranchSerializer


class UserSerializer(serializers.ModelSerializer):
    # created_by = serializers.HiddenField(default=serializers.CurrentUserDefault(), required=False)

    class Meta:
        model = CustomUser
        fields = "__all__"

        extra_kwargs = {'password': {'write_only': True}}
        
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = super().create(validated_data)
        user.set_password(password)
        user.save()
        return user
    
    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        if password:
            instance.set_password(password)
        return super().update(instance, validated_data)


class CustomUserSerializer(UserSerializer):
    companies = serializers.PrimaryKeyRelatedField(many=True, queryset=cmpny_mastr.objects.all(), required=False)
    branches = serializers.PrimaryKeyRelatedField(many=True, queryset=brnch_mstr.objects.all(), required=False)
    branches = BranchSerializer(many=True, read_only=True)

    def init(self, *args, **kwargs):
        super().init(*args, **kwargs)
        
        if 'request' in self.context and self.context['request'].user.is_authenticated:
            self.fields['companies'] = serializers.PrimaryKeyRelatedField(many=True, queryset=cmpny_mastr.objects.all(), required=False)
            self.fields['branches'] = serializers.PrimaryKeyRelatedField(many=True, queryset=brnch_mstr.objects.all(), required=False)
        else:
            self.fields.pop('companies')
            self.fields.pop('branches')


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = '__all__'


class CustomUserGroupSerializer(serializers.ModelSerializer):
    # user = serializers.SerializerMethodField()
    class Meta:
        model = CustomUserGroup
        fields = '__all__'
    