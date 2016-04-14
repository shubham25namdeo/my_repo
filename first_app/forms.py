
from django import forms
from django.contrib.admin.widgets import AdminDateWidget
from django.forms import SelectDateWidget, DateField
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import ugettext_lazy as _

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.TextInput(attrs={'placeholder': 'E-mail address'}))
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username', 'password1', 'password2')


#clean email field
def clean_email(self):
    email = self.cleaned_data["email"]
    try:
        User._default_manager.get(email=email)
    except User.DoesNotExist:
        return email
    raise forms.ValidationError('duplicate email')

#modify save() method so that we can set user.is_active to False when we first create our user
def save(self, commit=True):
    user = super(RegistrationForm, self).save(commit=False)
    user.email = self.cleaned_data['email']
    if commit:
        user.is_active = False # not active until he opens activation link
        user.save()

    return user

class CommentForm(UserCreationForm):
    comment = forms.CharField(required=True)
    class Meta:
        fields = ('comment',)

class NotesForm(forms.ModelForm):
    notes = forms.CharField(required=True)
    class Meta:
        fields = ('notes','title',)
        model = Note


class ArtForm(forms.ModelForm):
      class Meta:
        fields = ('title','desc', 'docfile',)
        model = Art
        docfile = forms.FileField(
            label='Select a file',
        )


class ConsultantForm(forms.ModelForm):
      class Meta:
        fields = ('cname', 'projtype', 'location', 'joindate', 'resume', 'JD','log_user',)
        model = Consultant
        resume = forms.FileField(
            label='Upload A Resume',
        )

class WordForm(forms.ModelForm):
    class Meta:
        fields = ('texts',)
        model = Word