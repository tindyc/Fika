from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path("login", views.member_login, name="login"),
    path("logout", views.member_logout, name="logout"),
    path("register", views.member_registration, name="register"),
    path("profile/<user_id>", views.member_profile, name="profile"),
    path("profile_edit", views.member_edit, name="profile_edit"),
    path("password-change/", views.ChangePasswordView.as_view(), name="password_change"),
    path("password-reset/", views.ResetPasswordView.as_view(), name="password_reset"),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='authenticate/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='authenticate/password_reset_complete.html'), name='password_reset_complete'),
]
