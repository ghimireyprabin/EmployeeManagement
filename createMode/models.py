from django.db import models
from django.shortcuts import reverse
from django.core.validators import MaxValueValidator , MinValueValidator
from core.models import Department
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

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
	resources = models.FileField(upload_to='resources', blank=True, null=True)
	deadline = models.DateTimeField()
	assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='assigned_to_user')
	created_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='created_by_user')
	created_at = models.DateTimeField(auto_now_add=True)
	submitted = models.BooleanField(default=False)
	reviewed = models.BooleanField(default=False)
	review_id = models.PositiveIntegerField(blank=True, null=True)
	is_accepted = models.BooleanField(default=False)
	is_rejected = models.BooleanField(default=False)
	reject_feedback_id = models.PositiveIntegerField(blank=True, null=True)

	def __str__(self):
		return f'{self.department.name}-{self.title}'

	def get_absolute_url(self):
		return reverse('core:manager-dashboard')

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

	def save(self, *args, **kwargs):
		try:
			if self.submitted_by:
				task = Task.objects.get(pk=self.task.pk)
				if task.submitted == False:
					task.submitted = True

				if self.reviewed_by != None:
					if task.reviewed == False:
						task.reviewed = True
				task.save()
		except e:
			print(e)
		super(TaskReview, self).save(*args, **kwargs)

# updating review_id in Task model after task is submitted
@receiver(post_save, sender=TaskReview)
def update_taskreview_id(sender, instance, created, **kwargs):
	task = Task.objects.get(pk=instance.task.pk)
	task.review_id = instance.pk
	task.save()
	
class TaskRejectFeedback(models.Model):
	task = models.ForeignKey(Task, on_delete=models.CASCADE)
	rejected_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rejected_by_user')
	remarks = models.TextField()
	rejected_on = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f'{self.rejected_by.username}-{self.task.title}'

	def save(self, *args, **kwargs):
		try:
			task = Task.objects.get(pk=self.task.pk)
			if task.is_rejected == False:
				task.is_rejected = True
			task.save()
		except e:
			print(e)
		super(TaskRejectFeedback, self).save(*args, **kwargs)

# updating review_id in Task model after feedback is submitted
@receiver(post_save, sender=TaskRejectFeedback)
def update_taskreject_id(sender, instance, created, **kwargs):
	task = Task.objects.get(pk=instance.task.pk)
	task.reject_feedback_id= instance.pk
	task.save()