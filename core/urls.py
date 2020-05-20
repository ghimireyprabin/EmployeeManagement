from django.urls import path
from .views import index
from register import views as register_views

urlpatterns = [
    path('',index, name='index'),
    path('register', register_views.register, name='register'),
    
]
