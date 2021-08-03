from django import forms
from datetime import date
from .models import Book
from django.forms import ModelForm

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

class BookModelForm(ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'genre', 'language', 'author', 'summary', 'isbn']