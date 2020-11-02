from django.urls import path
from .views import *

app_name='assignment'
urlpatterns = [
	path('', adminIndex.as_view(), name='admin-index'),
    path('userlist/<int:pk>', userList.as_view(), name='userlist'),
    path('userprofile/<int:pk>', userProfile.as_view(), name='userprofile'),
    path('department-list', DepartmentList.as_view(), name='department-list'),
    path('unassigned-list', unassignedUserList.as_view(), name='unassigned-list'),
    path('assign-dept-manager', departmentManagerCreateView.as_view(), name='assign-dept-manager'),
    path('update-dept-manager/<int:pk>', departmentManagerUpdateView.as_view(), name='update-dept-manager'),
]
