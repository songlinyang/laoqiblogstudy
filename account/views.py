from django.shortcuts import render,redirect,reverse
from django.http import HttpResponse
from django.contrib.auth import authenticate,login
from .forms import LoginForm,RegistrationForm

# Create your views here.

def user_login(request):

    if request.method == "GET":
        login_form = LoginForm()
        return render(request,"account/login.html",{"form":login_form})
    elif request.method == "POST":
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user = authenticate(login_form.cleaned_data)
            if user:
                login(request,user)
                return HttpResponse("您已经登录成功....")
            else:
                return HttpResponse("您的用户名或密码错误，请重新登录")
        else:
            login_url = reverse("account:user_login")
            return redirect(login_url)

def register(request):
    if request.method == "GET":
        user_form = RegistrationForm()
        return render(request,"account/register.html",{"form":user_form})

    elif request.method == "POST":
        user_form = RegistrationForm()