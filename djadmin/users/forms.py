from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from .models import myuser


class RegisterForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = myuser
        fields = ('username', 'email')

    # check if email is valid
    def clean_email(self):
        email = self.cleaned_data['email']
        users = myuser.objects.filter(email=email)
        if users:
            raise forms.ValidationError("该邮箱已注册过，尝试登录？")
        return email


class ChangeInfoForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = myuser
        fields = ('username', 'email')



class LoginForm(forms.Form):
    username = forms.CharField(label='用户名')
    password = forms.CharField(label='密码', widget=forms.PasswordInput)



class UserProfileForm(forms.ModelForm):
    class Meta:
        model = myuser
        fields = ['username', 'email',]