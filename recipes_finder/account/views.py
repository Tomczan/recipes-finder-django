from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from .forms import LoginForm, UserRegistrationForm
from django.views import View

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
            return render(request,
                          'registration/register_done.html',
                          {'new_user': new_user})

    def get(self, request):
        registration_form = UserRegistrationForm()
        return render(request,
                      'registration/register.html',
                      {'registration_form': registration_form})
