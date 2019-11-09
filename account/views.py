from django.shortcuts import render,redirect,reverse
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth import authenticate,login
from .forms import LoginForm,RegistrationForm,UserProfileForm,UserInfoForm,UserForm
from django.contrib.auth.decorators import login_required
from .models import UserProfile,UserInfo
from django.contrib.auth.models import User

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
        phone_form = UserProfileForm()
        return render(request,"account/register.html",{"form":user_form,"profile":phone_form})

    elif request.method == "POST":
        user_form = RegistrationForm(request.POST)
        userprofile_form = UserProfileForm(request.POST)
        if user_form.is_valid() and userprofile_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password2'])
            new_user.save()
            new_profile = userprofile_form.save(commit=False)
            new_profile.user = new_user  #这里保存对应user_id的外键
            new_profile.save()
            print("new_user",new_user)
            #新增UserInfo关联的用户
            UserInfo.objects.create(user=new_user)

            login_url = reverse("account:user_login")
            return redirect(login_url)
        else:
            # print(user_form)
            # return render(request,"account/register.html",{"form",user_form})
            return HttpResponse("注册失败")

@login_required(login_url="/account/newlogin/")
def myself(request):
    if request.method == "GET":
        user = User.objects.get(username=request.user.username)
        print(user)
        userprofile = UserProfile.objects.get(user=user)
        userinfo = UserInfo.objects.get(user=user)
        return render(request,"account/myself.html",{"uesr":user,"userprofile":userprofile,"userinfo":userinfo})
    else:
        return HttpResponse("页面不存在")

@login_required(login_url="/account/newlogin/")
def myself_edit(request):
    user = User.objects.get(username=request.user.username)
    userprofile = UserProfile.objects.get(user=request.user)
    userinfo = UserInfo.objects.get(user=request.user)

    if request.method == "GET":
        user_form = UserForm(instance=request.user)
        userprofile_form = UserProfileForm(initial={"birth":userprofile.birth,"phone":userprofile.phone})
        userinfo_form = UserInfoForm(initial={"school":userinfo.school,"company":userinfo.company,"address":userinfo.address,"profession":userinfo.profession,"aboutme":userinfo.aboutme})
        return render(request,"account/myself_edit.html",{"user_form":user_form,"userprofile_form":userprofile_form,"userinfo_form":userinfo_form})
    elif request.method == "POST":
        user_form = UserForm(request.POST)
        userprofile_form = UserProfileForm(request.POST)
        userinfo_form = UserInfoForm(request.POST)
        if user_form.is_valid() and userprofile_form.is_valid() and userinfo_form.is_valid():
            user_cd = user_form.cleaned_data
            print("user_form.cleaned_data的值是:",user_form.cleaned_data)
            print("user_form.cleaned_data的类型是:",type(user_form.cleaned_data))
            print("user_cd的值是：",user_cd)
            userprofile_cd = userprofile_form.cleaned_data
            print(userprofile_cd)
            userinfo_cd = userinfo_form.cleaned_data
            # print(user_cd["email"])
            user.email = user_cd.get("email","")
            userprofile.birth = userprofile_cd.get("birth",None)
            userprofile.phone = userprofile_cd.get("phone","")
            userinfo.school = userinfo_cd.get("school","")
            userinfo.company = userinfo_cd.get("company","")
            userinfo.profession = userinfo_cd.get("profession","")
            userinfo.address = userinfo_cd.get("address","")
            userinfo.aboutme = userinfo_cd.get("aboutme","")

            user.save()
            userprofile.save()
            userinfo.save()

        userinfo_url = reverse("account:user_info")
        return HttpResponseRedirect(userinfo_url)
@login_required(login_url="/account/newlogin/")
def my_image(request):
    if request.method == "GET":
        return render(request,"account/imagecrop.html")
    elif request.method == "POST":
        img = request.POST.get("img","")
        if img:
            userinfo = UserInfo.objects.get(user=request.user.id)
            userinfo.photo = img
            userinfo.save()
            return HttpResponse("1")

        else:
            print("上传文件，没有获取到任何内容~")