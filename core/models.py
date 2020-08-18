from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

gender_choices = [
    ('M', 'Male'),
    ('F', 'Female'),
    ('O', 'Others')
]
working_hours_choices = [
	('F', 'Full Time'),
	('P', 'Part Time'),
	('c', 'Contract Based')
]
rank_choices = [
	('I', 'Intern'),
	('J', 'Junior'),
	('M', 'Mid-level'),
	('S', 'Senior')
]

class EmployeePersonalInfo(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	fullname = models.CharField(max_length=50)
	gender = models.CharField(max_length=25, choices=gender_choices)
	age = models.IntegerField()
	image = models.ImageField(default="default.png", upload_to='profile_pics')
	address = models.CharField(max_length=50)
	phone_number = models.CharField(max_length=15, validators=[RegexValidator(r'^\d{1,15}$')])

	def __str__(self):
		return self.user.username

class EmployeeEducationInfo(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	university = models.CharField(max_length=50)
	degree = models.CharField(max_length=50)
	faculty = models.CharField(max_length=50)
	graduatation_year = models.DateField()

	def __str__(self):
		return self.user.username

class EmployeeExperienceInfo(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	experience_in_years = models.IntegerField()
	no_of_previous_company = models.IntegerField()
	jobtitle_at_previous = models.CharField(max_length=50)

	def __str__(self):
		return self.user.username

class Department(models.Model):
	name = models.CharField(max_length=60)
	description = models.CharField(max_length=264)
	

	def __str__(self):
		return self.name

class Role(models.Model):
	name = models.CharField(max_length=60)
	description = models.CharField(max_length=264)

	def __str__(self):
		return self.name

class PayGrade(models.Model):
	grade = models.CharField(max_length=60)
	amount = models.PositiveIntegerField()

	def __str__(self):
		return self.grade

class EmployeeJobInfo(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	job_title = models.CharField(max_length=50)
	rank = models.CharField(max_length=25, choices=rank_choices)
	working_hours = models.CharField(max_length=25, choices=working_hours_choices)
	department = models.ForeignKey(Department, on_delete=models.SET_NULL, blank=True, null=True)
	roles = models.ForeignKey(Role, on_delete=models.SET_NULL, blank=True, null=True)
	Pay_Grade = models.ForeignKey(PayGrade, on_delete=models.SET_NULL, blank=True, null=True)


	def __str__(self):
		return self.user.username

	