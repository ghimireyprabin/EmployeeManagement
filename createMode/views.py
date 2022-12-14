from django.shortcuts import render, redirect
from django.views.generic import CreateView, UpdateView, DetailView
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from .forms import TaskForm, TaskReviewForm, TaskAssignForm
from core.models import *
from .models import Task, TaskReview, TaskRejectFeedback
from django. contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin

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

class RoleCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = Role
    fields = ['name', 'description']
    template_name = 'createMode/create_roles.html'
    success_url = reverse_lazy('assignment:rolelist')

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
class TaskCreateView(LoginRequiredMixin, ManagerRequiredMixin, CreateView):
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

# task create view (assigned to user)
class UserTaskCreate(LoginRequiredMixin,ManagerRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
   # fields = ['title', 'description', 'total_points', 'deadline', 'department', 'assigned_to']
    template_name = 'createMode/user_task_create.html'
    # success_url= redirect('core:manager-dashboard')

    def get_success_url(self):
        return reverse_lazy('core:manager-dashboard')

    def get_form_kwargs(self):
        """
        Returns the keyword arguments for instantiating the form.
        """
        kwargs = super(UserTaskCreate, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.assigned_to = User.objects.get(pk = self.kwargs.get('pk'))
        # department = EmployeeJobInfo.objects.get(user=self.request.user).department
        # form.instance.department = Department.objects.filter(pk = department.pk) 
        return super(UserTaskCreate, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = User.objects.get(pk = self.kwargs['pk'])
        personal_info = EmployeePersonalInfo.objects.get(user = user)
        
        context['username'] = user.username
        
        return context

class TaskUpdateView(LoginRequiredMixin, ManagerRequiredMixin, UpdateView):
    model = Task
    #fields = ['department', 'title', 'description', 'total_points', 'assigned_to', 'deadline']
    form_class = TaskForm
    template_name = 'createMode/update_task.html'
    
    def get_form_kwargs(self):
        """
        Returns the keyword arguments for instantiating the form.
        """
        kwargs = super(TaskUpdateView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs


    def form_valid(self, form):

        form.instance.submitted_by = self.request.user
        task_id = self.kwargs.get('pk')
        task = Task.objects.get(pk = task_id)
        
        # if TaskReview.objects.get(task = task):
        if task.reviewed:
            messages.add_message(self.request, messages.WARNING, 'Task already reviewed. You cannot make further changes.')
            return redirect('core:manager-dashboard')
            # return render(self.request, self.template_name, {
            #     'error': 'Task already submitted',
            #     'form': form
            # })

        elif task.is_accepted == True:
            messages.add_message(self.request, messages.WARNING, 'You cannot update this task. Task already accepted.')
            return redirect('core:manager-dashboard')

        else:
            if self.request.user.is_authenticated and self.request.user == task.created_by:
                form.instance.is_rejected = False
                messages.add_message(self.request, messages.SUCCESS, 'Task successfully updated')
                return super(TaskUpdateView, self).form_valid(form)
            else:
                messages.add_message(self.request, messages.WARNING, 'You are not authorized to modify this task.')
                return redirect('core:manager-dashboard')
                # return render(self.request, self.template_name, {
                # 'error': 'You are not assigned to this task.',
                # 'form': form
            # })

class TaskAssignView(LoginRequiredMixin, ManagerRequiredMixin, UpdateView):
    model = Task
    # fields = ['assigned_to']
    form_class = TaskAssignForm
    template_name = 'createMode/assign_task.html'
    
    def get_form_kwargs(self):
        """
        Returns the keyword arguments for instantiating the form.
        """
        kwargs = super(TaskAssignView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def form_valid(self, form):

        form.instance.submitted_by = self.request.user
        task_id = self.kwargs.get('pk')
        task = Task.objects.get(pk = task_id)
        
        # if TaskReview.objects.get(task = task):
        if task.reviewed:
            messages.add_message(self.request, messages.WARNING, 'Task already reviewed. You cannot make further changes.')
            return redirect('core:manager-dashboard')
            # return render(self.request, self.template_name, {
            #     'error': 'Task already submitted',
            #     'form': form
            # })
        else:
            if self.request.user.is_authenticated and self.request.user == task.created_by:
                form.instance.is_rejected = False
                messages.add_message(self.request, messages.SUCCESS, 'successfully assigned to task.')
                return super(TaskAssignView, self).form_valid(form)
            else:
                messages.add_message(self.request, messages.WARNING, 'You are not authorized to modify this task.')
                return redirect('core:manager-dashboard')
                # return render(self.request, self.template_name, {
                # 'error': 'You are not assigned to this task.',
                # 'form': form
            # })

class ReviewTask(ManagerRequiredMixin, UpdateView):
    model= TaskReview
    form_class = TaskReviewForm
    #fields = ['remarks', 'awarded_points']
    template_name = 'createMode/task_review.html'
    success_url = '/'

    def get_form_kwargs(self):
        """
        Returns the keyword arguments for instantiating the form.
        """
        kwargs = super(ReviewTask, self).get_form_kwargs()
        kwargs.update({'task_review_pk': self.kwargs['pk']})
        return kwargs

    def form_valid(self, form):
        form.instance.reviewed_by = self.request.user
        return super(ReviewTask, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        task_review_info = TaskReview.objects.get(pk=self.kwargs['pk'])
        task_info = task_review_info.task
        submitted_user_profile_id = EmployeeJobInfo.objects.get(user=task_review_info.submitted_by).pk
        
        # print(task_info.deadline-timedelta(hours=24))
        # if task_review_info.submitted_on > task_info.deadline:
        #     print('Late')
        # elif task_review_info.submitted_on < task_info.deadline-timedelta(1):
        #     print('early')
        # else:
        #     print('on time')

        context['task_review'] = task_review_info
        context['task'] = task_info
        context['submitted_user_profile_id']= submitted_user_profile_id
        
        return context

class submitTaskCreateView(CreateView):
    model = TaskReview
    template_name = 'createMode/submit_task.html'
    fields=['resources', 'submission_feedback']
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        task_info = Task.objects.get(pk=self.kwargs['pk'])
        
        context['task_info'] = task_info
        print(context)
        print(self.kwargs['pk'])
        
        return context

    def form_valid(self, form):

        form.instance.submitted_by = self.request.user
        task_id = self.kwargs.get('pk')
        task = Task.objects.get(pk = task_id)
        form.instance.task = task
        print(task)
        # if TaskReview.objects.get(task = task):
        if TaskReview.objects.filter(task=task).exists():
            messages.add_message(self.request, messages.WARNING, 'Task already submitted')
            return redirect('core:index')
            # return render(self.request, self.template_name, {
            #     'error': 'Task already submitted',
            #     'form': form
            # })
        else:
            if self.request.user.is_authenticated and self.request.user == task.assigned_to:
                return super(submitTaskCreateView, self).form_valid(form)
            else:
                messages.add_message(self.request, messages.WARNING, 'You are not assigned to this task.')
                return render(self.request, self.template_name, {
                'error': 'You are not assigned to this task.',
                'form': form
            })

class TaskAcceptView(LoginRequiredMixin, UpdateView):
    model = Task
    template_name = 'createMode/accept_task.html'
    fields=['is_accepted']
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        task_info = Task.objects.get(pk=self.kwargs['pk'])
        
        context['task_info'] = task_info
        
        return context

    def form_valid(self, form):

        task_id = self.kwargs.get('pk')
        task = Task.objects.get(pk = task_id)
        # check if task is already accepted
        if task.is_accepted == True:
            messages.add_message(self.request, messages.WARNING, 'Task already accepted.')
            return redirect('core:index')
        elif task.is_rejected == True:
            messages.add_message(self.request, messages.WARNING, 'Task already rejected.')
            return redirect('core:index')
        else:
            if self.request.user.is_authenticated and self.request.user == task.assigned_to:
                form.instance.is_accepted = True
                messages.add_message(self.request, messages.SUCCESS, 'Task accepted.')
                return super(TaskAcceptView, self).form_valid(form)
            else:
                messages.add_message(self.request, messages.WARNING, 'You are not assigned to this task.')
                return redirect('core:index')

class TaskRejectView(LoginRequiredMixin, CreateView):
    model = TaskRejectFeedback
    template_name = 'createMode/reject_task.html'
    fields=['remarks']
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        task_info = Task.objects.get(pk=self.kwargs['pk'])
        
        context['task_info'] = task_info
        
        return context

    def form_valid(self, form):

        form.instance.rejected_by = self.request.user
        task_id = self.kwargs.get('pk')
        task = Task.objects.get(pk = task_id)
        form.instance.task = task
        
        # if TaskReview.objects.get(task = task):
        if task.is_rejected == True:
            messages.add_message(self.request, messages.WARNING, 'Task already rejected')
            return redirect('core:index')
        elif task.is_accepted == True:
            messages.add_message(self.request, messages.WARNING, 'Task already accepted.')
            return redirect('core:index')
        else:
            if self.request.user.is_authenticated and self.request.user == task.assigned_to:
                messages.add_message(self.request, messages.WARNING, 'Task rejected.')
                return super(TaskRejectView, self).form_valid(form)
            else:
                messages.add_message(self.request, messages.WARNING, 'You are not assigned to this task.')
                return redirect('core:index')

class TaskRejectDetailsView(LoginRequiredMixin, ManagerRequiredMixin, DetailView):
    model = TaskRejectFeedback
    context_object_name = 'rejected_task_feedback'
    template_name = 'createMode/rejected_feedback.html'

