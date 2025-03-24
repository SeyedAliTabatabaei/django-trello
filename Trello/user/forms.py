from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *

class SignUpForm(UserCreationForm):
    username = forms.CharField(label='',required=True,widget=forms.TextInput(attrs={'placeholder':'نام کاربری'}))
    email = forms.EmailField(label='',required=True,widget=forms.EmailInput(attrs={'placeholder':'ایمیل خود را وارد کنید'}))
    password1 = forms.CharField(label='',required=True,widget=forms.PasswordInput(attrs={'placeholder':'گذرواژه '}))
    password2 = forms.CharField(label='',required=True,widget=forms.PasswordInput(attrs={'placeholder':'تکرار گذرواژه'}))

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100, label='Username')
    password = forms.CharField(widget=forms.PasswordInput, label='Password')

class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['name']

class TeamForm(forms.ModelForm):
    members_usernames = forms.CharField(
        label="یوزرنیم اعضا (با کاما جدا کنید)", required=False
    )
    name = forms.CharField(
        label="نام تیم",
    )

    class Meta:
        model = Team
        fields = ['name', 'members_usernames']

    def clean_members_usernames(self):
        usernames = self.cleaned_data["members_usernames"]
        if usernames:
            usernames_list = [username.strip() for username in usernames.split(",")]
            users = User.objects.filter(username__in=usernames_list)
            if len(users) != len(usernames_list):
                raise forms.ValidationError("برخی از یوزرنیم‌ها پیدا نشدند!")
            return users
        return []

class BoardForm(forms.ModelForm):
    name = forms.CharField(label='',widget=forms.TextInput(attrs={'placeholder': 'نام بورد'}))
    description = forms.CharField(label='',widget=forms.Textarea(attrs={'placeholder': 'توضیحات','class':'form-control'}))
    class Meta:
        model = Board
        fields = ['name', 'description']

class ListForm(forms.ModelForm):

    name = forms.CharField(
        label="نام لیست",
    )
    class Meta:
        model = List
        fields = ['name']


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["name", "description", "start_date", "end_date", "due_date", "is_completed","assigned_users"]
        widgets = {
            "start_date": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "end_date": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "due_date": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "assigned_users" :forms.CheckboxSelectMultiple,

        }
 
