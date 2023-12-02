from django import forms
from django.forms import BaseFormSet
from supplier.models import Supplier
from items.models import OrderedItem, IssuedItem
from .models import Order, Staff, Receiver, Issuer, BatchInventory

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
                raise forms.ValidationError("Receiver role not found for the current user.")
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
                raise forms.ValidationError("Issuer role not found for the current user.")
        return cleaned_data

class TransferItemForm(forms.ModelForm):
    receiver_batch_number = forms.ModelChoiceField(queryset=BatchInventory.objects.all())

    class Meta:
        model = IssuedItem
        fields = ['batch_number', 'item'] 

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
 
    def clean(self):
        cleaned_data = super().clean()
        item = cleaned_data.get('item')
        source_batch_number = cleaned_data.get('batch_number')
        receiver_batch_number = cleaned_data.get('receiver_batch_number')
        if receiver_batch_number == source_batch_number:
            raise forms.ValidationError("Cannot transfer to the same batch")

        if self.request and self.request.user.is_authenticated:
            try:
                staff = Staff.objects.get(staff_number=self.request.user.username)
            except Staff.DoesNotExist:
                raise forms.ValidationError("Staff role not found for the current user.")

        return cleaned_data