import ssl
from decouple import config
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail, BadHeaderError
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from .forms import Registration, LoginForm, EditForm, ResetPassword, ContactUs, CommentForm
from .models import ProfileModel, CommentsModel
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import DetailView
from django.http import Http404, HttpResponse
import smtplib

my_email = "ainurminu@mail.ru"
password = config('MAIL_PASSWORD')


# Create your views here.
def homepage(request):
    if request.method == 'POST':
        if 'message' in request.POST:
            form = ContactUs(request.POST)
            if form.is_valid():
                form.save()
                subject = 'GoSpeakClub Contact Us'
                body = {
                    'full_name': form.cleaned_data['full_name'],
                    'email': form.cleaned_data['email'],
                    'message': form.cleaned_data['message']
                }
                message = '\n'.join(body.values())
                context = ssl.create_default_context()
                with smtplib.SMTP_SSL('smtp.mail.ru', 465, context=context) as connection:
                    try:
                        connection.login(my_email, password)
                        connection.sendmail(my_email, "specialforpy@gmail.com",
                                            f"Subject:{subject}\n\n{message}")
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                # try:
                #     send_mail(subject, message, 'admin@example.com', ['admin@example.com'], fail_silently=False)
                messages.success(request, 'Your message was successfully sent! We will reply soon.')
                return redirect('club:index')
        if 'comment' in request.POST:
            form = CommentForm(request.POST)
            if form.is_valid():
                new_comment = form.save(commit=False)
                new_comment.user = request.user
                new_comment.save()
                messages.success(request, 'Your comment is ready for publishing and awaits moderation to approve it.')
    contact_form = ContactUs()
    comment_form = CommentForm()
    comments = CommentsModel.objects.filter(approved=True)[:5]
    return render(request, 'club/index.html', {
        'contact_form': contact_form,
        'comment_form': comment_form,
        'comments': comments,
    })


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
                        'domain': 'https://gospeakclub.herokuapp.com/',
                        'site_name': 'speaking_club',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        context = ssl.create_default_context()
                        with smtplib.SMTP_SSL('smtp.mail.ru', 465, context=context) as connection:
                            connection.login(my_email, password)
                            connection.sendmail(my_email, [user.email],
                                                f"Subject:{subject}\n\n{email}")
                        # send_mail(subject, email, 'specialforpy@gmail.com', [user.email], fail_silently=False)
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                messages.success(request, 'A message with reset password instructions has been sent to your email.')
                return redirect("club:index")
    password_reset_form = ResetPassword()
    return render(request=request, template_name="club/password/password_reset.html",
                  context={"form": password_reset_form})
