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
from .forms import Registration, LoginForm, EditForm, ResetPassword, ContactUs, CommentForm, AccessForm, HomeworkSubmitForm, HomeworkFilesForm
from .models import ProfileModel, CommentsModel, HomeworkSubmitModel, HomeworkFilesModel, ChatMessages
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import DetailView
from django.http import Http404, HttpResponse
import smtplib

my_email = "ainurminu@mail.ru"
password = config('MAIL_PASSWORD')
access_code = 'GL14'


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
                        'domain': 'gospeakclub.herokuapp.com',
                        'site_name': 'speaking_club',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'https',
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
            else:
                messages.error(request, 'There are no accounts signed up with this email.')
    password_reset_form = ResetPassword()
    return render(request=request, template_name="club/password/password_reset.html",
                  context={"form": password_reset_form})


@login_required
def course_page(request):
    if request.method == 'POST':
        form = AccessForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            if code == access_code:
                request.user.profilemodel.access = True
                request.user.profilemodel.save()
            else:
                messages.error(request, 'Invalid code. Please, try again.')
    access = request.user.profilemodel.access
    if not access:
        form = AccessForm()
        return render(request, 'club/access.html', {'form': form})
    status_s = HomeworkSubmitModel.status_type_submit(request.user)
    status_a = HomeworkSubmitModel.status_type_accepted(request.user)
    status_d = HomeworkSubmitModel.status_type_denied(request.user)
    total_score = ProfileModel.objects.get(user=request.user).total_score
    days_completed = HomeworkSubmitModel.days_completed(request.user)
    return render(request, 'club/course_hp.html', {'status_s': status_s, 'status_a': status_a, 'status_d': status_d, 'score': total_score, 'days_completed': days_completed})


@login_required
def course_day(request, day):
    if request.method == 'POST':
        submit_form = HomeworkSubmitForm(request.POST)
        files_form = HomeworkFilesForm(request.POST, request.FILES)
        files = request.FILES.getlist('file')
        if submit_form.is_valid() and files_form.is_valid():
            new_homework = submit_form.save(commit=False)
            new_homework.user = request.user
            new_homework.day = day
            new_homework.status = 'S'
            new_homework.save()
            for file in files:
                f = HomeworkFilesModel(homework=new_homework, file=file)
                f.save()
            messages.success(request, 'Your homework has been successfully submitted!')
        return redirect(f'club:course_day', day=day)
    submit_form = HomeworkSubmitForm()
    files_form = HomeworkFilesForm()
    return render(request, f'club/course_days/day{day}.html', {'submit_form': submit_form, 'files_form': files_form})


@login_required
def course_chat(request):
    page = 'general'
    chat_messages = ChatMessages.objects.filter(page=page)[0:25]
    return render(request, 'club/course_chat.html', {'messages': chat_messages})
