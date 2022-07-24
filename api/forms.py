from .serializers import BookSerializer
from django import forms


class BookForm(forms.Form):
    book_ordering = forms.IntegerField()
    novel = forms.CharField(max_length=255)
    author = forms.CharField(max_length=150)
    country = forms.CharField(max_length=30)
