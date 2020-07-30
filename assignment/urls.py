from django.urls import path
from .views import *

app_name='assignment'
urlpatterns = [
    path('', AdminCrud.as_view(), name='admincrud'),
    path('userprofile/<int:pk>', userProfile.as_view(), name='userprofile'),
    path('department-list', DepartmentList.as_view(), name='department-list')
]
