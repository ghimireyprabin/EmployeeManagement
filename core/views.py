from django.shortcuts import render,redirect
from django.views import View 
from django.views.generic import ListView, DetailView, CreateView, UpdateView,DeleteView, TemplateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth import authenticate, login


from .models import *
from createMode.models import *
from .forms import * 
from django.contrib import messages
from django.contrib.auth.decorators import login_required



class AdminRequiredMixin(object):
    def dispatch(self, request, *args, **kwargs):
        usr = request.user
        if usr.is_authenticated and usr.is_superuser:
            pass
        else:
            return redirect('/register/')

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

class LoginView(FormView):
    template_name = 'core/login.html'
    form_class = LoginForm
    success_url = '/admincrud'

    def form_valid(self, form):
        uname = form.cleaned_data['username']
        pword = form.cleaned_data['password']

        user = authenticate(username=uname, password=pword)
        self.thisuser = user
        if user is not None:
            login(self.request, user)
        else:
            return render(self.request, self.template_name, {
                'error': 'your username doesnot exist',
                'form': form
            })
        return super().form_valid(form)

@login_required(login_url='/login')
def index(request):
	# checking if employee information are updated
	EPIRecord = EmployeePersonalInfo.objects.filter(user= request.user)
	
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

	isManager = False
	EJI = EmployeeJobInfo.objects.filter(user = request.user)
	
	if EJI and EJI[0].isManager == True:
		isManager = True

	tasks = Task.objects.filter(assigned_to = request.user)
	
	context = {
		'assigned_tasks' : tasks.filter(submitted = False),
		'submitted_tasks' : tasks.filter(submitted = True),
		'isManager' : isManager,
	}

	return render(request, 'core/index.html', context)

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

# EmployeePersonalInfo(EPI) Update view
class EPIUpdateView(UpdateView, LoginRequiredMixin,UserPassesTestMixin):
	model = EmployeePersonalInfo
	fields = ['fullname', 'gender', 'age', 'address', 'phone_number']
	template_name = 'core/epicreate.html'
	success_url = '/profile'

	def user_passes_test(self, request):
		if request.user.is_authenticated:
		    self.object = self.get_object()
		    return self.object.user == request.user
		return False

	def dispatch(self, request, *args, **kwargs):
		if request.user.is_authenticated:
	
			EmployeePersonalInfo_data = EmployeePersonalInfo.objects.filter(user=self.request.user)
			
			if not self.user_passes_test(request):
				if not EmployeePersonalInfo_data:
					return redirect('core:add-personal-info')
				return redirect('core:update-personal-info', pk=EmployeePersonalInfo_data[0].pk)
		
		return super(EPIUpdateView, self).dispatch(
	    request, *args, **kwargs)

# EmployeeProfilePics(EPI) Update view
class ProfilePicIUpdateView(UpdateView, LoginRequiredMixin,UserPassesTestMixin):
	model = EmployeePersonalInfo
	fields = ['image']
	template_name = 'core/epicreate.html'
	success_url = '/profile'

	def user_passes_test(self, request):
		if request.user.is_authenticated:
		    self.object = self.get_object()
		    return self.object.user == request.user
		return False

	def dispatch(self, request, *args, **kwargs):
		if request.user.is_authenticated:
			EmployeePersonalInfo_data = EmployeePersonalInfo.objects.filter(user=self.request.user)
			
			if not self.user_passes_test(request):
				if not EmployeePersonalInfo_data:
					return redirect('core:add-personal-info')
				return redirect('core:update-profile-pic', pk=EmployeePersonalInfo_data[0].pk)
		return super(ProfilePicIUpdateView, self).dispatch(
	    request, *args, **kwargs)

# Details of a task review
class TaskReviewDeailView(DetailView, LoginRequiredMixin):
	model = TaskReview
	template_name = 'core/review_details.html'
	context_object_name = 'review'

class ManagerDashboard(ListView, LoginRequiredMixin, ManagerRequiredMixin):
	model = Task
	template_name = 'core/manager_dashboard.html'
	context_object_name = 'tasks'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		tasks = Task.objects.filter(created_by = self.request.user)
		print(tasks)

		context['created_tasks'] = tasks.filter(assigned_to = None)
		context['assigned_tasks'] = tasks.exclude(assigned_to = None).filter(submitted = False)
		context['submitted_tasks'] = tasks.filter(submitted = True)		

		return context	


#view for admin Access and roles that will be used later 

# class AdminRole(View):
# 	''' Admin's role maybe '''

# 	a = str(roles_admin[0])
# 	if a == "admin":
# 		print ("hello")


class AdminCrud(AdminRequiredMixin, TemplateView):
	template_name = "crud.html"

