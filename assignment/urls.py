from django.urls import path
from .views import *

app_name='assignment'
urlpatterns = [
    path('', AdminCrud.as_view(), name='admincrud')
]
