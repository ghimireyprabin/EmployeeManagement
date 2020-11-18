from django.db import models
from django.core.validators import MaxValueValidator , MinValueValidator
from core.models import Department
from django.contrib.auth.models import User

submission_choices = [
    ('Early', 'Early'),
    ('On-Time', 'On-Time'),
    ('Late', 'Late')
]

class Task(models.Model):
	title = models.CharField(max_length=240)
	description = models.TextField()
	total_points = models.PositiveIntegerField(validators=[MinValueValidator(10), MaxValueValidator(100)])
	department = models.ForeignKey(Department, on_delete=models.CASCADE)
	deadline = models.DateTimeField()
	assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='assigned_to_user')
	created_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='created_by_user')
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f'{self.department.name}-{self.title}'

class TaskReview(models.Model):
	task = models.ForeignKey(Task, on_delete=models.CASCADE)
	submitted_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='submitted_by_user')
	submitted_on = models.DateTimeField(auto_now_add=True)
	reviewed_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='reviewed_by_user')
	reviewed_on = models.DateTimeField(auto_now=True)
	remarks = models.TextField(blank=True, null=True)
	awarded_points = models.PositiveIntegerField(validators=[MinValueValidator(10), MaxValueValidator(100)],blank=True, null=True)
	submission = models.CharField(max_length=25, choices=submission_choices, blank=True, null=True)

	def __str__(self):
		return f'{self.submitted_by.username}-{self.task.title}'