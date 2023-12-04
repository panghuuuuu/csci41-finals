from django import forms
from django.forms import BaseFormSet
from items.models import SoldItem
from .models import *

class SalesItemForm(forms.ModelForm):
    class Meta:
        model = SoldItem
        fields = ['item', 'sold_quantity']
   
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        item = cleaned_data.get('item')
        sold_quantity = cleaned_data.get('sold_quantity')

        return cleaned_data

