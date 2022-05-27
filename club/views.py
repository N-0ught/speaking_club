from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail, BadHeaderError
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from .forms import Registration, LoginForm, EditForm, ResetPassword, ContactUs
from .models import ProfileModel
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import DetailView
from django.http import Http404, HttpResponse


# Create your views here.
def homepage(request):
    if request.method == 'POST':
        form = ContactUs(request.POST)
        if form.is_valid():
            subject = 'GoSpeakClub Contact Us'
            body = {
                'full_name': form.cleaned_data['full_name'],
                'email': form.cleaned_data['email'],
                'message': form.cleaned_data['message']
            }
            message = '\n'.join(body.values())
            try:
                send_mail(subject, message, 'admin@example.com', ['admin@example.com'], fail_silently=False)
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            messages.info(request, 'Your message was successfully sent! We will reply soon.')
            return redirect('club:index')
    form = ContactUs()
    return render(request, 'club/index.html', {'form': form})


def register(request):
    if request.method == 'POST':
        form = Registration(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            ProfileModel.objects.create(user=user)
            messages.success(request,
                             f'Registration successful. Now please go to <a href="/profile/">your profile</a> and '
                             f'edit your profile '
                             'information.')
            return redirect('club:index')
        else:
            for error in form.errors:
                messages.error(request, form.errors[error])
    form = Registration()
    return render(request, 'club/register.html', {'form': form})


def login_request(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f'You are now logged in as {username}.')
                return redirect('club:index')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = LoginForm()
    return render(request, 'club/login.html', {'form': form})


@login_required
def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("club:index")


class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = ProfileModel
    template_name = 'club/profile.html'

    def get_object(self):
        return self.request.user.profilemodel


@login_required
def edit(request):
    obj = get_object_or_404(ProfileModel, user=request.user)
    if request.method == 'POST':
        form = EditForm(request.POST or None, instance=obj)
        if form.is_valid():
            form.save()
            return redirect('club:profile')
    form = EditForm(instance=obj)
    return render(request, 'club/edit.html', {'form': form})


def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = ResetPassword(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "club/password/password_reset_email.txt"
                    c = {
                        "email": user.email,
                        'username': user.username,
                        'domain': '127.0.0.1:8000',
                        'site_name': 'speaking_club',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email, 'admin@example.com', [user.email], fail_silently=False)
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                    messages.success(request, 'A message with reset password instructions has been sent to your email.')
                return redirect("club:index")
    password_reset_form = ResetPassword()
    return render(request=request, template_name="club/password/password_reset.html",
                  context={"form": password_reset_form})
