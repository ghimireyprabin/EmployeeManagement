from django.shortcuts import render, redirect
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from core.models import *

class AdminRequiredMixin(object):
    def dispatch(self, request, *args, **kwargs):
        usr = request.user
        if usr.is_authenticated and usr.is_superuser:
            pass
        else:
            return redirect('core:index')

        return super().dispatch(request, *args, **kwargs)

class DepartmentCreateView(AdminRequiredMixin, CreateView):
	model = Department
	fields = ['name', 'description']
	template_name = 'createMode/create-department.html'
	success_url = reverse_lazy('assignment:department-list')

class DepartmentUpdateView(AdminRequiredMixin, UpdateView):
    model = Department
    fields = ['name', 'description']
    template_name = 'createMode/create-department.html'
    success_url = reverse_lazy('assignment:department-list')