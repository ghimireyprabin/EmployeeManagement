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

