from django import forms
from .models import Task, TaskReview
from django.contrib.auth.models import User
from core.models import *

class TaskForm(forms.ModelForm):
	deadline = forms.DateTimeField(
        input_formats=['%d/%m/%Y %H:%M'],
        widget=forms.DateTimeInput(attrs={
            'class': 'form-control datetimepicker-input',
            'data-target': '#datetimepicker1'
        })
       )

	class Meta:
		model = Task
		fields = ('department', 'title', 'description', 'total_points', 'assigned_to', 'deadline')

	def __init__(self, *args, **kwargs):
		department = EmployeeJobInfo.objects.filter(user=kwargs.pop('user'))[0].department
		super(TaskForm, self).__init__(*args, **kwargs)
		self.fields['department'].queryset = Department.objects.filter(pk = department.pk)
		self.fields['assigned_to'].queryset = User.objects.select_related('employeejobinfo').filter(employeejobinfo__department=department)

class TaskReviewForm(forms.ModelForm):

	class Meta:
		model = TaskReview 
		fields = ('remarks', 'awarded_points', 'submission')

	def __init__(self, *args, **kwargs):
		# task_pk = kwargs.pop('task_pk')
		task_review = TaskReview.objects.get(pk=kwargs.pop('task_review_pk'))
		task_maxvalue = task_review.task.total_points
		super(TaskReviewForm, self).__init__(*args, **kwargs)
		
		
		self.fields['awarded_points'] = forms.IntegerField(min_value = 10, max_value=task_maxvalue)

class TaskAssignForm(forms.ModelForm):

	class Meta:
		model = Task 
		fields = ('assigned_to',)

	def __init__(self, *args, **kwargs):
		department = EmployeeJobInfo.objects.filter(user=kwargs.pop('user'))[0].department
		super(TaskAssignForm, self).__init__(*args, **kwargs)
		self.fields['assigned_to'].queryset = User.objects.select_related('employeejobinfo').filter(employeejobinfo__department=department)
