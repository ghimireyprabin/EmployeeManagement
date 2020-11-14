from django import forms
from .models import Task
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