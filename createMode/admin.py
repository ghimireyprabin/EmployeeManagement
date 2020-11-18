from django.contrib import admin
from .models import Task, TaskReview

# Register your models here.

admin.site.register(Task)
admin.site.register(TaskReview)