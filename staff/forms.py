from django import forms
from django.forms import BaseFormSet
from supplier.models import Supplier
from items.models import OrderedItem, IssuedItem
from .models import Order, Staff, Receiver, Issuer

class OrderedItemForm(forms.ModelForm):
    class Meta:
        model = OrderedItem
        fields = ['item', 'order_quantity']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        item = cleaned_data.get('item')
        order_quantity = cleaned_data.get('order_quantity')
        if self.request and self.request.user.is_authenticated:
            try:
                staff = Staff.objects.get(staff_number=self.request.user.username)
                receiver = Receiver.objects.get(staff=staff)
            except Receiver.DoesNotExist:
                raise forms.ValidationError("Receiver not found for the current user.")
        return cleaned_data

class IssuanceItemForm(forms.ModelForm):
    class Meta:
        model = IssuedItem
        fields = ['item', 'issued_quantity', 'issued_SRP']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        supplier_item = cleaned_data.get('supplier_item')
        issued_quantity = cleaned_data.get('issued_quantity')
        issued_SRP = cleaned_data.get('issued_SRP')
        if self.request and self.request.user.is_authenticated:
            try:
                staff = Staff.objects.get(staff_number=self.request.user.username)
                issuer = Issuer.objects.get(staff=staff)
            except Issuer.DoesNotExist:
                raise forms.ValidationError("Issuer not found for the current user.")
        return cleaned_data