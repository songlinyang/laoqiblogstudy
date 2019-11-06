from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = "account"

urlpatterns = [
    path('login/',views.user_login,name="login"),
    path('newlogin/',auth_views.LoginView.as_view(template_name="account/login.html"),name="user_login"),
    path('logout/',auth_views.LogoutView.as_view(),name="user_logout"),
    path('register/',views.register,name="register"),
    path('password-change/',auth_views.PasswordChangeView.as_view(template_name="account/password_change_form.html",
                                                                  success_url="/account/password-change-done/"),name="password_change"),
    path('password-change-done/',auth_views.PasswordChangeDoneView.as_view(template_name="account/password_change_done.html"),name="password_change_done"),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name="account/password_reset_form.html",
                                                                 email_template_name="account/password_reset_email.html",
                                                                 subject_template_name="account/password_reset_subject.txt",
                                                                 success_url="/account/password-reset-done/"),name='password_reset'),
    path('password-reset-done/', auth_views.PasswordResetDoneView.as_view(template_name="account/password_reset_done.html"), name='password_reset_done'),

    path('password-reset-confirm/(?P<uidb64>[-\w]+)/(?P<token>[-/w]+)/', auth_views.PasswordResetConfirmView.as_view(template_name="account/password_reset_confirm.html",
                                                                                success_url="/account/password-reset-complete/"), name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name="account/password_reset_complete.html",
                                                                                  ), name='password_reset_complete'),
]