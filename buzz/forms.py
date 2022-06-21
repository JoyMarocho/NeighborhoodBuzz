from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User, Profile, Post, Neighborhood, Business
from django.forms.widgets import TextInput, FileInput, NumberInput, Textarea
from django.contrib.auth import get_user_model

User = get_user_model()

#Your form details here
class NewUserForm(UserCreationForm):

    class Meta:
        model = User
        fields = ("email", "password1","password2")

    def save(self,commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class ExistingUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('email',)

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('image','user','bio','location')

class NeighborhoodForm(forms.ModelForm):
    class Meta:
        model = Neighborhood
        fields = ('name', 'location', 'population')
        widgets = {
            'name': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your neighborhood name'
            }),
            'location': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your neighborhood location'
            }),
            'population': NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your neighborhood population'
            }),
        }

class BusinessForm(forms.ModelForm):
    class Meta:
        model = Business
        fields = ['name', 'email_address', 'description', 'user','neighborhood']
        
        widgets = {
            'name': TextInput(attrs={'class': 'form-control', 'placeholder': 'Name'}),
            'email_address': TextInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'description': TextInput(attrs={'class': 'form-control', 'placeholder': 'Description'}),
        }