from django.http import HttpResponse
from django.shortcuts import  render, redirect
from django.contrib.auth import login, authenticate
from django.contrib import messages #import messages
from .models import User, PasswordReset
from django.contrib.auth.forms import AuthenticationForm
from django.core.mail import send_mail, BadHeaderError
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes, force_text
from Details.models import Follower
# Create your views here.

def index(request):
    #return HttpResponse("Welcome, this is the SMA app")
	return render (request=request, template_name="home.html")

def register_request(request):
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		confirmpwd = request.POST['conf_password']
		first_name = request.POST['first_name']
		last_name = request.POST['last_name']
		email = request.POST['email']
		
		if password == confirmpwd:
			try:
				user = User.objects.get(email=email)
				messages.error(request, "Email already exists")
				return redirect("register")
			except User.DoesNotExist:
				user = User.objects.create_user(email=email, username=username, password=password, first_name=first_name, last_name=last_name)
				user.save()
				messages.success(request, "Registration successful")
				return redirect("index")
		messages.error(request, "Unsuccessful registration. Invalid information.")
	return render(request=request, template_name="register.html")




def login_request(request):
	if request.user.is_authenticated:
		return redirect("index")

	if request.method == "POST":
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				messages.info(request, f"You are now logged in as {username}.")
				return redirect("index")
			else:
				messages.error(request,"Invalid username or password.")
		else:
			messages.error(request,"Invalid username or password.")	
	return render(request=request, template_name="login.html")	




def password_reset_request(request):
	if request.method == "POST":
		email = request.POST['email']
		user = User.objects.filter(email=email).first()

		# Record token in PasswordReset model
		token = default_token_generator.make_token(user)
		passwordResetModel = PasswordReset.objects.create(user_id=user, token=token)
		passwordResetModel.save()

		# Create and send e-mail
		subject = "Password Reset Requested"
		email_template_name = "password_reset_email.txt"
		c = {
			"email": user.email,
			"domain": "127.0.0.1:8000",
			"site_name": "SMA Team 2", 
			"uid": urlsafe_base64_encode(force_bytes(user.pk)),
			"user": user,
			"token": token,
			"protocol": "http",
		}

		email = render_to_string(email_template_name, c)
		try:
			send_mail(subject, email, "team2@sma.com", [user.email], fail_silently=False)
		except BadHeaderError:
			return HttpResponse("Invalid header found.")
		return redirect("password_reset_done")
	
	return render(request=request, template_name="password_reset.html")


def password_reset_done_request(request):
	return render(request=request, template_name="password_reset_done.html")


def password_reset_confirm_request(request, uidb64, token):
	user_id = force_text(urlsafe_base64_decode(uidb64))
	user = User.objects.filter(id=user_id).first()

	if request.method == "POST":
		password = request.POST['password']
		confirmpwd = request.POST['conf_password']
		
		if password == confirmpwd:
			user.set_password(password)
			user.save()
			
			passwordResetModel = PasswordReset.objects.filter(user_id=user, token=token).first()
			passwordResetModel.token_used = True
			passwordResetModel.save()

			return render(request=request, template_name="password_reset_complete.html")
		else:
			messages.error(request, "Passwords do not match.")

	else:
		passwordResetModel = PasswordReset.objects.filter(user_id=user, token=token).first()

		if passwordResetModel.token_used == True:
			return HttpResponse("Token has already been used.")

	return render(request=request, template_name="password_reset_confirm.html")
	
def password_reset_complete_request(request):
	return render(request=request, template_name="password_reset_complete.html")



def follow_user(request, user_name):
    other_user = User.objects.get(name=user_name)
    session_user = request.session['user']
    get_user = User.objects.get(name=session_user)
    check_follower = Follower.objects.get(user=get_user.id)
    is_followed = False
    if other_user.name != session_user:
        if check_follower.another_user.filter(name=other_user).exists():
            add_usr = Follower.objects.get(user=get_user)
            add_usr.another_user.remove(other_user)
            is_followed = False
            return redirect(f'/profile/{session_user}')
        else:
            add_usr = Follower.objects.get(user=get_user)
            add_usr.another_user.add(other_user)
            is_followed = True
            return redirect(f'/profile/{session_user}')

        return redirect(f'/profile/{session_user}')
    else:
        return redirect(f'/profile/{session_user}')
