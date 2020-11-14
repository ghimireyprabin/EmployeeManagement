from django.shortcuts import render, redirect
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from .forms import TaskForm
from core.models import *
from .models import Task

class AdminRequiredMixin(object):
    def dispatch(self, request, *args, **kwargs):
        usr = request.user
        if usr.is_authenticated and usr.is_superuser:
            pass
        else:
            return redirect('core:index')

        return super().dispatch(request, *args, **kwargs)

class ManagerRequiredMixin(object):
    def dispatch(self, request, *args, **kwargs):
        usr = request.user
        usr_job_info = EmployeeJobInfo.objects.get(user=usr)
        if usr.is_authenticated and usr_job_info.isManager:
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

class JobInfoCreateView(AdminRequiredMixin, CreateView):
    model = EmployeeJobInfo
    fields = ['user', 'job_title', 'rank', 'working_hours', 'department', 'roles', 'Pay_Grade', 'isManager']
    template_name = 'createMode/jobinfo_form.html'
    success_url = reverse_lazy('assignment:department-list')

class JobInfoUpdateView(AdminRequiredMixin, UpdateView):
    model = EmployeeJobInfo
    fields = ['user', 'job_title', 'rank', 'working_hours', 'department', 'roles', 'Pay_Grade', 'isManager']
    template_name = 'createMode/jobinfo_form.html'
    success_url = reverse_lazy('assignment:department-list')

# task create view
class TaskCreateView(ManagerRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
   # fields = ['title', 'description', 'total_points', 'deadline', 'department', 'assigned_to']
    template_name = 'createMode/task_create.html'
    success_url='/'

    def get_form_kwargs(self):
        """
        Returns the keyword arguments for instantiating the form.
        """
        kwargs = super(TaskCreateView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super(TaskCreateView, self).form_valid(form)