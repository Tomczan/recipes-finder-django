from django.urls import path
from .views import user_login
from django.contrib.auth import views as auth_views

app_name = 'account'

urlpatterns = [
    # path('login/', user_login.as_view(), name='login')
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
