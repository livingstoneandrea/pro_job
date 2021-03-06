from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, Education_level, Employment_details, File_uploaded, Preference


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=100, help_text='First Name')
    last_name = forms.CharField(max_length=100, help_text='Last Name')
    email = forms.EmailField(max_length=150, help_text='Email')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2',)


class Profile_InfoForm(ModelForm):
    class Meta:
        model = Profile
        exclude =['user','signup_confirmation','employment_details','education_level','Preference','file_upload']


class Education_levelForm(ModelForm):
    class Meta:
        model = Education_level
        fields = '__all__'


class Employement_DetailForm(ModelForm):
    class Meta:
        model = Employment_details
        fields = '__all__'


class Preference_Form(ModelForm):
    class Meta:
        model = Preference
        fields = '__all__'
class File_UploadForm(ModelForm):

    class Meta:
        model = File_uploaded
        fields = '__all__'
