from django.contrib import admin
from .models import Farmer,HindiFarmerDetails,MarathiFarmerDetails,PunjabiFarmerDetail,TeleguFarmerDetails
# Register your models here.
admin.site.register(Farmer)
admin.site.register(HindiFarmerDetails)
admin.site.register(MarathiFarmerDetails)
admin.site.register(PunjabiFarmerDetail)
admin.site.register(TeleguFarmerDetails)


