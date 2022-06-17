from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from .forms import LoginForm
from django.views import View

# Create your views here.


class user_login(View):
    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=form['username'],
                                password=form['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Uwierzytelnianie pomyślne')
                else:
                    return HttpResponse('Konto jest zablokowane')
        else:
            return HttpResponse('Nieprawidłowe dane uwierzytelniajace')

    def get(self, request):
        form = LoginForm()
        return render(request, 'account/login.html', {'form': form})
