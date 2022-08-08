from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from .views import RegisterView, UserEmailEditView, UserAndProfileEditView

app_name = 'account'

# https://docs.djangoproject.com/en/4.0/topics/auth/default/#all-authentication-views
urlpatterns = [
    # path('login/', user_login.as_view(), name='login')
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('password_reset/',
         auth_views.PasswordResetView.as_view(
             success_url=reverse_lazy('account:password_reset_done')),
         name='password_reset'),
    path('password_reset/done/',
         auth_views.PasswordResetDoneView.as_view(),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             success_url=reverse_lazy('account:password_reset_complete')),
         name='password_reset_confirm'),
    path('reset/done/',
         auth_views.PasswordResetCompleteView.as_view(),
         name='password_reset_complete'),
    path('settings/password/',
         auth_views.PasswordChangeView.as_view(
             template_name='account\settings\password.html'),
         name='password_change'),
    path('password_change/done/',
         auth_views.PasswordChangeDoneView.as_view(),
         name='password_change_done'),
    path('registration/', RegisterView.as_view(), name='register'),
    path('settings/email/', UserEmailEditView.as_view(), name='email_change'),
    path('settings/profile/', UserAndProfileEditView.as_view(),
         name='profile_info_change'),
]
