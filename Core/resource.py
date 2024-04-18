from import_export import resources,fields
from .models import cntry_mstr



class CountryResource(resources.ModelResource):
    class Meta:
        model = emp_master
        fields = ('id','country_code','country_name')
        