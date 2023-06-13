from django.shortcuts import render, redirect
from django.contrib.auth.models import User

def chatPage(request, *args, **kwargs):
	if not request.user.is_authenticated:
		return redirect("login-user")

	users = User.objects.exclude(username=request.user.username)
	context = {'users': users}
	# print(context)
	return render(request, "chatPage.html", context)
