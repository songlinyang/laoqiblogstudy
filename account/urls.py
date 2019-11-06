from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = "account"

urlpatterns = [
    path('login/',views.user_login,name="login"),
    path('newlogin/',auth_views.LoginView.as_view(),name="user_login"),
    path('logout/',auth_views.LogoutView.as_view(),name="user_logout"),
    path('register/',views.register,name="register"),
    path('password_change/',auth_views.PasswordChangeView.as_view(template_name="account/password_change_form.html",success_url="/account/password_change_done/"),name="password_change"),
    path('password_change_done/',auth_views.PasswordChangeDoneView.as_view(template_name="account/"),name="password_change_done"),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]