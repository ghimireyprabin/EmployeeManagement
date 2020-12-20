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

	assigned_tasks = tasks.filter(is_accepted = False).filter(is_rejected = False)
	accepted_tasks = tasks.filter(is_accepted = True).filter(submitted = False)
	rejected_tasks = tasks.filter(is_rejected = True)
	submitted_tasks = TaskReview.objects.filter(submitted_by = request.user)
	
	context = {
		'assigned_tasks' : assigned_tasks,
		'total_assigned_tasks' : assigned_tasks.count(),
		'accepted_tasks' : accepted_tasks,
		'total_accepted_tasks' : accepted_tasks.count(),
		'rejected_tasks' : rejected_tasks,
		'total_rejected_tasks' : rejected_tasks.count(),
		'submitted_tasks' : submitted_tasks,
		'total_submitted_tasks' : submitted_tasks.count(),

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

# Details of a task
class TaskDeailView(DetailView, LoginRequiredMixin):
	model = Task
	template_name = 'core/task_details.html'
	context_object_name = 'task'

# Details of a task review
class TaskReviewDeailView(DetailView, LoginRequiredMixin):
	model = TaskReview
	template_name = 'core/review_details.html'
	context_object_name = 'review'

class ManagerDashboard(LoginRequiredMixin, ManagerRequiredMixin, ListView):
	model = Task
	template_name = 'core/manager_dashboard.html'
	context_object_name = 'tasks'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		tasks = Task.objects.filter(created_by = self.request.user)
		
		context['created_tasks'] = tasks.filter(assigned_to = None)
		context['assigned_tasks'] = tasks.filter(submitted = False).filter(is_accepted = False).filter(is_rejected = False).exclude(assigned_to = None)
		context['accepted_tasks'] = tasks.filter(is_accepted = True).filter(submitted = False)
		context['rejected_tasks'] = tasks.filter(is_rejected = True)
		context['submitted_tasks'] = TaskReview.objects.filter(task__created_by = self.request.user)		

		return context	

class DepartmentInformation(LoginRequiredMixin, ManagerRequiredMixin, ListView):
	model = Department
	template_name = 'core/department_info.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)

		job_info = EmployeeJobInfo.objects.get(user = self.request.user)
		if job_info.isManager == True:    
			department = job_info.department
			user_info = EmployeeJobInfo.objects.filter(department = department)
			employee_info = []
			for user in user_info:
				info = EmployeePersonalInfo.objects.get(user =user.user)
				
				emp_info = {
					'user_pk' : user.user.pk,
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
					'isManager' : user.isManager,
				}
				employee_info.append(emp_info)
			context['employee_info'] = employee_info
			context['department'] = department

			return context
		else:
			context['error_message'] = 'You are not authorized to visit this page.'
			return context

class TaskList(LoginRequiredMixin, ListView):
	model = Task
	template_name = 'core/task_list.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)

		job_info = EmployeeJobInfo.objects.get(user = self.request.user)
		task_user = User.objects.get(pk = self.kwargs['pk'])

		if job_info.isManager == True or self.request.user == task_user:
			tasks = Task.objects.filter(assigned_to = task_user).order_by('created_at')

			context['tasks'] = tasks
			context['total_assigned_tasks'] = tasks.filter(is_accepted = False).filter(is_rejected = False).count()
			context['total_accepted_tasks'] = tasks.filter(is_accepted = True).filter(submitted = False).count()
			context['total_submitted_tasks'] = tasks.filter(submitted = True).count()
			context['total_rejected_tasks'] = tasks.filter(is_rejected = True).count()
			context['username'] = task_user.username
			user_personal_info = EmployeePersonalInfo.objects.filter(user = task_user)
			if user_personal_info:
				context['fullname'] = user_personal_info[0].fullname
			
			return context
		else:
			context['error_message'] = 'You are not authorized to visit this page.'
			return context

#view for admin Access and roles that will be used later 

# class AdminRole(View):
# 	''' Admin's role maybe '''

# 	a = str(roles_admin[0])
# 	if a == "admin":
# 		print ("hello")


class AdminCrud(AdminRequiredMixin, TemplateView):
	template_name = "crud.html"

