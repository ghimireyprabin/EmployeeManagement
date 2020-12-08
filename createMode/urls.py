from django.urls import path
from .views import *

app_name='createMode'
urlpatterns = [
    path('department', DepartmentCreateView.as_view(), name='create-departent'),
    path('department-update/<int:pk>', DepartmentUpdateView.as_view(), name='update-department'),
    path('jobinfo-update/<int:pk>', JobInfoUpdateView.as_view(), name='jobinfo-update'),
    path('jobinfo-create', JobInfoCreateView.as_view(), name='jobinfo-create'),
    path('create-task', TaskCreateView.as_view(), name='create-task'),
    path('user-create-task/<int:pk>', UserTaskCreate.as_view(), name='user-create-task'),    
    path('update-task/<int:pk>', TaskUpdateView.as_view(), name='update-task'),
    path('assign-task/<int:pk>', TaskAssignView.as_view(), name='assign-task'),
    path('task-review/<int:pk>', ReviewTask.as_view(), name='task-review'),
    path('submit-task/<int:pk>', submitTaskCreateView.as_view(),name='submit-task'),
    path('role', RoleCreateView.as_view(), name='create-role'),
    path('accept-task/<int:pk>', TaskAcceptView.as_view(),name='accept-task'),
    path('reject-task/<int:pk>', TaskRejectView.as_view(),name='reject-task'),
    path('rejected-feedback/<int:pk>', TaskRejectDetailsView.as_view(),name='rejected-feedback'),

]
