from django.shortcuts import render, redirect
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from .forms import TaskForm, TaskReviewForm
from core.models import *
from .models import Task, TaskReview
from django. contrib import messages

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
    fields=['remarks']
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