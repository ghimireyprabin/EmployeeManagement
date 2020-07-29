from django.shortcuts import render, redirect
from django.views.generic import ListView
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


class AdminCrud(AdminRequiredMixin, ListView):
	template_name = "assignment/index.html"
	model = EmployeePersonalInfo

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)    
		context['department'] = Department.objects.all()
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
