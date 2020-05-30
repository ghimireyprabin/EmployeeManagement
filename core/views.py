from django.shortcuts import render,redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required

@login_required(login_url='/login')
def index(request):
	# checking if employee information are updated
	EPIRecord = EmployeePersonalInfo.objects.get(user= request.user)
	if not EPIRecord:
		messages.info(request, f'Please update your personal information.')
		return redirect('core:add-personal-info')
	EEIRecord = EmployeeEducationInfo.objects.filter(user= request.user)
	if not EEIRecord:
		messages.info(request, f'Please update your educational information.')
		return redirect('core:add-education-info')
	EExIRecord = EmployeeExperienceInfo.objects.filter(user= request.user)
	if not EExIRecord:
		messages.info(request, f'Please update your experience information.')
		return redirect('core:add-experience-info')

	return render(request, 'core/index.html')

# EmployeePersonalInfo(EPI) create view
class EPICreateView(CreateView, LoginRequiredMixin):
	model = EmployeePersonalInfo
	fields = [ 'fullname', 'gender', 'age', 'address', 'phone_number']
	template_name = 'core/epicreate.html'
	success_url = '/'

	def form_valid(self, form):
		form.instance.user = self.request.user
		return super().form_valid(form)

# EmployeeEducationInfo(EEI) create view
class EEICreateView(CreateView, LoginRequiredMixin):
	model = EmployeeEducationInfo
	fields = [ 'university', 'degree', 'faculty', 'graduatation_year']
	template_name = 'core/eeicreate.html'
	success_url = '/'

	def form_valid(self, form):
		form.instance.user = self.request.user
		return super().form_valid(form)

# EmployeeExperienceInfo(EExI) create view
class EExICreateView(CreateView, LoginRequiredMixin):
	model = EmployeeExperienceInfo
	fields = [ 'experience_in_years', 'no_of_previous_company', 'jobtitle_at_previous']
	template_name = 'core/eexicreate.html'
	success_url = '/'

	def form_valid(self, form):
		form.instance.user = self.request.user
		return super().form_valid(form)

@login_required(login_url='/login')
def profile(request):
	# checking if employee information is updated
	EPIRecord = EmployeePersonalInfo.objects.filter(user= request.user)
	if not EPIRecord:
		messages.info(request, f'Please update your personal information.')
		return redirect('core:add-personal-info')

	personal_info = EmployeePersonalInfo.objects.get(user=request.user)
	try:
		job_info = EmployeeJobInfo.objects.get(user=request.user)
	except:
		job_info = {
			'department' : 'N/A',
			'job_title' : 'N/A',
			'rank' : 'N/A',
			'working_hours' : 'N/A',
			'roles' : 'N/A',
			'Pay_Grade' : 'N/A'
		}
	user_info = request.user

	context = {
		'personal_info' : personal_info,
		'job_info' : job_info, 
		'user_info' : user_info
	}

	return render(request, 'core/profile.html', context)
