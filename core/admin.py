from django.contrib import admin
from .models import *

admin.site.register(EmployeePersonalInfo)
admin.site.register(EmployeeEducationInfo)
admin.site.register(EmployeeExperienceInfo)
admin.site.register(EmployeeJobInfo)