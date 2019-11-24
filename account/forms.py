from django import forms
from django.contrib.auth.models import User
from account.models import UserProfile,UserInfo
"""
<tr><th><label for="id_username">Username:</label></th><td><input type="text" name="username" required id="id_username"></td></tr>
<tr><th><label for="id_password">Password:</label></th><td><input type="password" name="password" required id="id_password"></td></tr>
"""

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(label="密码",widget=forms.PasswordInput)
    password2 = forms.CharField(label="确认密码",widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ("username","email")

    # 调用is_valid()会触发
    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError("请再次确认密码")
        return cd['password2']

class UserProfileForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ("phone",)

class UserInfoForm(forms.ModelForm):

    class Meta:
        model = UserInfo
        fields = ("school","company","profession","address","aboutme","photo")

class UserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ("email",)
