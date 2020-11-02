from django.contrib import admin
from .models import *

admin.site.register(EmployeePersonalInfo)
admin.site.register(EmployeeEducationInfo)
admin.site.register(EmployeeExperienceInfo)
admin.site.register(EmployeeJobInfo)
admin.site.register(Department)
admin.site.register(Role)
admin.site.register(PayGrade)
admin.site.register(DepartmentManager)