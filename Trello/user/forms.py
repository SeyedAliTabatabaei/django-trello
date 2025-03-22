from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

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
    class Meta:
        model = Board
        fields = ['name', 'description']

class ListForm(forms.ModelForm):
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
 