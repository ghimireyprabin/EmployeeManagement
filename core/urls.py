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

    path('register', register_views.register, name='register'),
    # path('login/', LoginView.as_view(), name='login'),

    path('admincrud/', AdminCrud.as_view(), name='admincrud'),

    
]
