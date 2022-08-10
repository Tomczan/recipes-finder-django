from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views import View

from .forms import (LoginForm, ProfileUpdateForm, UserUpdateForm,
                    UserEmailUpdateForm, UserPasswordUpdateForm,
                    UserRegistrationForm)

# Create your views here.


# class UserLogin(View):
#     def post(self, request):
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             cd = form.cleaned_data
#             user = authenticate(username=cd['username'],
#                                 password=cd['password'])
#             if user is not None:
#                 if user.is_active:
#                     login(request, user)
#                     return HttpResponse('Authentication completed successfully')
#                 else:
#                     return HttpResponse('Account is locked')
#         else:
#             return HttpResponse('Invalid credentials')

#     def get(self, request):
#         form = LoginForm()
#         return render(request, 'account/login.html', {'form': form})

class RegisterView(View):
    def post(self, request):
        registration_form = UserRegistrationForm(request.POST)
        if registration_form.is_valid():
            new_user = registration_form.save(commit=False)
            new_user.set_password(registration_form.cleaned_data['password'])
            new_user.save()
            messages.success(
                request, f'Account created for {new_user.username}! Now you can log-in.')
            return redirect('account:login')
            # return render(request,
            #               'registration/register_done.html',
            #               {'new_user': new_user})

    def get(self, request):
        registration_form = UserRegistrationForm()
        return render(request,
                      'registration/register.html',
                      {'registration_form': registration_form})


class UserAndProfileUpdateView(LoginRequiredMixin, View):
    login_url = 'account:login'

    def post(self, request):
        user_form = UserUpdateForm(instance=request.user,
                                   data=request.POST)
        profile_form = ProfileUpdateForm(instance=request.user.profile,
                                         data=request.POST,
                                         files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
        return render(request,
                      'account/settings/profile_info_change.html',
                      {'user_form': user_form,
                       'profile_form': profile_form})

    def get(self, request):
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)
        return render(request,
                      'account/settings/profile_info_change.html',
                      {'user_form': user_form,
                       'profile_form': profile_form})


class UserEmailUpdateView(LoginRequiredMixin, View):
    login_url = 'account:login'

    def post(self, request):
        email_form = UserEmailUpdateForm(instance=request.user,
                                         data=request.POST)
        if email_form.is_valid():
            email_form.save()
            messages.success(request, f'Email changed successfully')
        return render(request,
                      'account/settings/email_change.html',
                      {'email_form': email_form})

    def get(self, request):
        email_form = UserEmailUpdateForm(instance=request.user)
        return render(request,
                      'account/settings/email_change.html',
                      {'email_form': email_form})


# class UserPasswordChangeView(LoginRequiredMixin, View):
#     login_url = 'account:login'

#     def post(self, request):
#         password = UserEmailUpdateForm(instance=request.user,
#                                      data=request.POST)
#         if email_form.is_valid():
#             email_form.save()
#             messages.success(request, f'Email changed successfully')
#         return render(request,
#                       'account/settings/email_change.html',
#                       {'email_form': email_form})

#     def get(self, request):
#         email_form = UserEmailUpdateForm(instance=request.user)
#         return render(request,
#                       'account/settings/email_change.html',
#                       {'email_form': email_form})
