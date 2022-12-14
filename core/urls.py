from django.urls import path
from .views import *
from register import views as register_views

app_name='core'
urlpatterns = [
    path('',index, name='index'),
    path('add-personal-info', EPICreateView.as_view(), name='add-personal-info'),
    path('add-education-info', EEICreateView.as_view(), name='add-education-info'),    
    path('add-experience-info', EExICreateView.as_view(), name='add-experience-info'),    
    path('profile', profile, name='profile'),
    path('update-personal-info/<int:pk>', EPIUpdateView.as_view(), name='update-personal-info'),
    path('update-profile-pic/<int:pk>', ProfilePicIUpdateView.as_view(), name='update-profile-pic'),
    path('task-review-details/<int:pk>', TaskReviewDeailView.as_view(), name='task-review-details'),
    path('manager-dashboard', ManagerDashboard.as_view(), name='manager-dashboard'),
    path('department-information', DepartmentInformation.as_view(), name='department-information'),
    path('task-list/<int:pk>', TaskList.as_view(), name='task-list'),
    path('task-details/<int:pk>', TaskDeailView.as_view(), name='task-details'),
    path('emp-performance/<int:pk>', EmpPerformance.as_view(), name='emp-performance'),

    path('register', register_views.register, name='register'),
    # path('login/', LoginView.as_view(), name='login'),

    path('admincrud/', AdminCrud.as_view(), name='admincrud'),

    
]
