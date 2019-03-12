from django import forms
from .models import SearchWord
class SearchWordFrom(forms.ModelForm):
    class Meta:
        model = SearchWord
        fields = ['word', 'flag']