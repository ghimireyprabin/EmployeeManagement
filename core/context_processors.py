from .models import EmployeeJobInfo

def check_authorization(request):
	if request.user.is_superuser:
		user_is_admin = True
	else:
		user_is_admin = False
	if request.user.is_authenticated:
		user_is_authenticated = True
		jobinfo = EmployeeJobInfo.objects.filter(user = request.user)[0]
		if jobinfo and jobinfo.isManager == True:
			user_is_manager = True
		else:
			user_is_manager = False
	else:
		user_is_authenticated = False
		user_is_manager = False

	return {
		'user_is_authenticated' : user_is_authenticated,
		'user_is_admin': user_is_admin,
		'user_is_manager' : user_is_manager,
	}