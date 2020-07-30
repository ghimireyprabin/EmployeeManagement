from django.urls import path
from .views import *

app_name='createMode'
urlpatterns = [
    path('department', DepartmentCreateView.as_view(), name='create-departent'),
    path('department-update/<int:pk>', DepartmentUpdateView.as_view(), name='update-department'),
]
