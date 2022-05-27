from django.urls import path
from . import views, forms
from django.contrib.auth import views as auth_views

app_name = 'club'
urlpatterns = [
    path('', views.homepage, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.login_request, name='login'),
    path('logout/', views.logout_request, name='logout'),
    path('profile/', views.ProfileDetailView.as_view(), name='profile'),
    path('profile/edit/', views.edit, name='edit'),
    path('password_reset/', views.password_reset_request, name='password_reset'),
    # path('password_reset/done/',
    #      auth_views.PasswordResetDoneView.as_view(template_name='club/password/password_reset_done.html'),
    #      name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='club/password/password_reset_confirm.html', form_class=forms.ConfirmResetPassword),
         name='password_reset_confirm'),
]