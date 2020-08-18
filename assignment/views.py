from django.shortcuts import render, redirect
from django.views.generic import ListView, TemplateView
from django.contrib.auth.models import User
from core.models import *

class AdminRequiredMixin(object):
    def dispatch(self, request, *args, **kwargs):
        usr = request.user
        if usr.is_authenticated and usr.is_superuser:
            pass
        else:
            return redirect('core:index')

        return super().dispatch(request, *args, **kwargs)


class adminIndex(AdminRequiredMixin, TemplateView):
	template_name = "assignment/index.html"

class userList(AdminRequiredMixin, ListView):
	template_name = "assignment/userlist.html"
	model = EmployeePersonalInfo

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)    
		department = Department.objects.get(pk= self.kwargs['pk'])
		job_info = EmployeeJobInfo.objects.filter(department = department)
		employee_info = []
		for user in job_info:
			info = EmployeePersonalInfo.objects.get(user =user.user)
			emp_info = {
				'username' : info.user.username,
				'fullname' : info.fullname,
				'age' : info.age,
				'address' : info.address,
				'pk' : info.pk,
				'department' : department,
				'job_title' : user.job_title,
				'rank' : user.rank,
				'working_hours' : user.working_hours,
				'roles' : user.roles,

			}
			employee_info.append(emp_info)
		context['employee_info'] = employee_info

		return context

class userProfile(AdminRequiredMixin, ListView):
	template_name = "core/profile.html"
	model = User

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)   
		context['personal_info'] = EmployeePersonalInfo.objects.get(pk= self.kwargs['pk'])
		context['user_info'] = context['personal_info'].user
		try:
			context['job_info'] = EmployeeJobInfo.objects.get(user=user_info)
		except:
			context['job_info'] = {
				'department' : 'N/A',
				'job_title' : 'N/A',
				'rank' : 'N/A',
				'working_hours' : 'N/A',
				'roles' : 'N/A',
				'Pay_Grade' : 'N/A'
			}
		if self.request.user != context['user_info']:
			context['is_logged_profile'] = False
		return context

class DepartmentList(AdminRequiredMixin, ListView):
	template_name = "assignment/departmentlist.html"
	model = Department
	context_object_name = 'department'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)    
		context['department'] = Department.objects.all()
		context['department_count'] = []
		for dept in context['department']:
			count = {
				'department_name': dept.name,
				'count' : EmployeeJobInfo.objects.filter(department=dept).count()
			}
			context['department_count'].append(count)
		return context

class unassignedUserList(AdminRequiredMixin, ListView):
	template_name = "assignment/userlist.html"
	model = EmployeePersonalInfo

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)    
		job_info = EmployeeJobInfo.objects.filter(department=None)
		employee_info = []
		for user in job_info:
			info = EmployeePersonalInfo.objects.get(user =user.user)
			emp_info = {
				'username' : info.user.username,
				'fullname' : info.fullname,
				'age' : info.age,
				'address' : info.address,
				'pk' : info.pk,
				'department' : user.department,
				'job_title' : user.job_title,
				'rank' : user.rank,
				'working_hours' : user.working_hours,
				'roles' : user.roles

			}
			employee_info.append(emp_info)
		context['employee_info'] = employee_info

		return context