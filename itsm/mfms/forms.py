from django.forms import ModelForm
from django import forms
from .models import Author, Book
class CalendarWidget(forms.TextInput):
    class Media:
        css = {
            'all': ('css/bootstrap.min.css', 'css/bootstrap-icons.css', 'css/jquery-confirm.min.css')
        }
        js = ('js/jquery-3.6.1.min.js', 'js/bootstrap.bundle.min.js', 'js/jquery-confirm.min.js')
class AuthorForm(ModelForm):
    class Meta:
        model = Author
        fields = ['name', 'title', 'birth_date']
        labels = {
            'title': '称谓',
            'name': '姓名',
            'birth_date': '生日',
        }
        widgets = {
            'title': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'birth_date': forms.TextInput(attrs={'class': 'form-control'}),
        }

class BookForm(ModelForm):
    class Meta:
        model = Book
        fields = ['name', 'authors']