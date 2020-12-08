from .models import EmployeeJobInfo, EmployeePersonalInfo

def check_authorization(request):
	if request.user.is_superuser:
		user_is_admin = True
	else:
		user_is_admin = False
	if request.user.is_authenticated:
		user_is_authenticated = True
		personalinfo = EmployeePersonalInfo.objects.filter(user = request.user)
		if personalinfo:
			personalinfo = personalinfo[0]
		jobinfo = EmployeeJobInfo.objects.filter(user = request.user)
		if jobinfo:
			jobinfo = jobinfo[0]
		if jobinfo and jobinfo.isManager == True:
			user_is_manager = True
		else:
			user_is_manager = False
		if personalinfo:
			user_fullname = personalinfo.fullname
		else:
			user_fullname = request.user.username
	else:
		user_is_authenticated = False
		user_is_manager = False
		user_fullname = None

	return {
		'user_is_authenticated' : user_is_authenticated,
		'user_is_admin': user_is_admin,
		'user_is_manager' : user_is_manager,
		'user_fullname' : user_fullname,
	}