from django import forms
from datetime import date
from .models import Book, BookInstance
from django.forms import ModelForm
#from django.contrib.auth import password_validation
#from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

class AuthorsForm(forms.Form):
    first_name = forms.CharField(label="Имя автора", max_length=100)
    last_name = forms.CharField(label="Фамилия автора", max_length=100)
    date_of_birth = forms.DateField(label="Дата рождения",
                                    initial=format(date.today()),
                                    widget=forms.widgets.DateInput(attrs={'type': 'date'}))
    date_of_death = forms.DateField(label="Дата смерти",
                                    initial=format(date.today()),
                                    widget=forms.widgets.DateInput(attrs={'type': 'date'}))
    biographi = forms.CharField(label="Биография", max_length=2000, widget=forms.Textarea)

class BookModelInstance(ModelForm):
    class Meta:
        model = BookInstance
        fields = ['adress','status', 'borrower', 'due_back']

class BookModelForm(ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'genre', 'language', 'author', 'summary', 'isbn']

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']