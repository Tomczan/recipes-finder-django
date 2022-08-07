import profile
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views import View

from .forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm, UserEmailEditForm

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


@login_required
class UserAndProfileEditView(View):
    def post(self, request):
        user_form = UserEditForm(instance=request.user,
                                 data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile,
                                       data=request.POST,
                                       files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
        return render(request,
                      'account/edit.html',
                      {'user_form': user_form,
                       'profile_form': profile_form})

    def get(self, request):
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
        return render(request,
                      'account/edit.html',
                      {'user_form': user_form,
                       'profile_form': profile_form})


class UserEmailEditView(View):
    @method_decorator(login_required(login_url='login'))
    def post(self, request):
        profile_form = UserEmailEditForm(instance=request.user.profile,
                                         data=request.POST)
        if profile_form.is_valid():
            profile_form.save()
        return render(request,
                      'account/settings/email.html',
                      {'profile_form': profile_form})

    @method_decorator(login_required(login_url='login'))
    def get(self, request):
        profile_form = UserEmailEditForm(instance=request.user.profile)
        return render(request,
                      'account/settings/email.html',
                      {'profile_form': profile_form})
