from django.db import models

# Create your models here.
#COMPANY MODEL
class cmpny_mastr(models.Model):

    cmpny_name = models.CharField(max_length=100,unique=True)
    cmpny_is_active = models.BooleanField(default=True)
    # country_id = models.ForeignKey('cntry_mstr',on_delete = models.CASCADE)
    cmpny_state_id = models.ForeignKey("Core.state_mstr",on_delete=models.CASCADE)
    cmpny_city = models.CharField(max_length=50)
    cmpny_pincode = models.CharField(max_length=20)
    cmpny_nmbr_1 = models.CharField(max_length=20,unique=True)
    cmpny_nmbr_2 = models.CharField(max_length=20,blank=True,null=True)
    cmpny_mail = models.EmailField(unique=True)
    cmpny_logo = models.ImageField(upload_to='logos',null=True)
    cmpny_fax =models.CharField(max_length=100,null=True,blank=True)
    cmpny_gst =models.CharField(max_length=100,null=True,blank=True)
    cmpny_country = models.ForeignKey("Core.cntry_mstr",on_delete=models.SET_DEFAULT, default="1")  # Many-to-many relationship with Country model
    cmpny_created_at = models.DateTimeField(auto_now_add=True)
    cmpny_created_by = models.ForeignKey('UserManagement.CustomUser', on_delete=models.SET_NULL, null=True, related_name='%(class)s_created_by')
    cmpny_updated_at = models.DateTimeField(auto_now=True)
    cmpny_updated_by = models.ForeignKey('UserManagement.CustomUser', on_delete=models.SET_NULL, null=True, related_name='%(class)s_updated_by')
    # cmpny_ADMIN_UID = models.ForeignKey('CustomUser', on_delete=models.SET_NULL,null=True)
    def __str__(self):
        return self.cmpny_name

    def save(self, *args, **kwargs):
        # Save the company
        super(cmpny_mastr, self).save(*args, **kwargs)

        # Create a corresponding branch
        brnch_mstr.objects.create(
            branch_name=self.cmpny_name,  # Set branch name to company name (you can customize this)
            br_company_id=self,
            br_is_active=self.cmpny_is_active,
            br_state_id=self.cmpny_state_id,
            br_city=self.cmpny_city,
            br_pincode=self.cmpny_pincode,
            br_branch_nmbr_1=self.cmpny_nmbr_1,
            br_branch_nmbr_2=self.cmpny_nmbr_2,
            br_branch_mail=self.cmpny_mail,
            br_country=self.cmpny_country,
            br_created_by=self.cmpny_created_by,
            br_updated_by=self.cmpny_updated_by
            # Add other fields as needed
        )
    
    

#branch model
class brnch_mstr(models.Model):
    branch_name = models.CharField(max_length=100)
    br_company_id = models.ForeignKey("cmpny_mastr",on_delete=models.CASCADE,null=True,blank=True)
    br_is_active = models.BooleanField(default=True)
    # country_id = models.ForeignKey('cntry_mstr',on_delete = models.CASCADE)
    br_state_id = models.ForeignKey("Core.state_mstr",on_delete=models.SET_DEFAULT, default="1", null=True)  
    br_city = models.CharField(max_length=50)
    br_pincode = models.CharField(max_length=20)
    br_branch_nmbr_1 = models.CharField(max_length=20,unique=True)
    br_branch_nmbr_2 = models.CharField(max_length=20,blank=True, null=True)
    br_branch_mail = models.EmailField(unique=True)
    br_country = models.ForeignKey("Core.cntry_mstr",on_delete=models.SET_DEFAULT, default="1", null=True) 
    br_created_at = models.DateTimeField(auto_now_add=True)
    br_created_by = models.ForeignKey('UserManagement.CustomUser', on_delete=models.CASCADE, null=True, related_name='%(class)s_created_by')
    br_updated_at = models.DateTimeField(auto_now=True)
    br_updated_by = models.ForeignKey('UserManagement.CustomUser', on_delete=models.SET_NULL, null=True, related_name='%(class)s_updated_by')
    def __str__(self):
        return self.branch_name
    

#departments model
class dept_master(models.Model):
    dept_name = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('UserManagement.CustomUser', on_delete=models.SET_NULL, null=True, related_name='%(class)s_created_by')
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey('UserManagement.CustomUser', on_delete=models.SET_NULL, null=True, related_name='%(class)s_updated_by')
    is_active = models.BooleanField(default=True)
    branch_id = models.ForeignKey("brnch_mstr", on_delete=models.SET_NULL, null=True)
    def __str__(self):
        return self.dept_name

#designation master
class desgntn_master(models.Model):
    job_title =  models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('UserManagement.CustomUser', on_delete=models.SET_NULL, null=True, related_name='%(class)s_created_by')
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey('UserManagement.CustomUser', on_delete=models.SET_NULL, null=True, related_name='%(class)s_updated_by')
    is_active = models.BooleanField(default=True)
    def __str__(self):
        return self.job_title

#CATOGARY master
class ctgry_master(models.Model):
    catogary_title =  models.CharField(max_length=50)
    ctgry_description = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('UserManagement.CustomUser', on_delete=models.SET_NULL, null=True, related_name='%(class)s_created_by')
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey('UserManagement.CustomUser', on_delete=models.SET_NULL, null=True, related_name='%(class)s_updated_by')
    is_active = models.BooleanField(default=True)
    def __str__(self):
        return self.catogary_title
    

class FiscalYear(models.Model):
    company_id = models.ForeignKey("cmpny_mastr",on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    start_date = models.DateField()

class FiscalPeriod(models.Model):
    fiscal_year = models.ForeignKey(FiscalYear, on_delete=models.CASCADE)
    period_number = models.PositiveIntegerField()
    start_date = models.DateField()
    end_date = models.DateField()
    company = models.ForeignKey("cmpny_mastr", on_delete=models.CASCADE, related_name='fiscal_periods')
    class Meta:
        unique_together = ('fiscal_year', 'period_number')


#LANGUAGE MASTER 
class LanguageMaster(models.Model):
    language = models.CharField(max_length=50)
    def __str__(self):
        return self.language