from django import forms
from django.forms import BaseFormSet
from supplier.models import Supplier
from items.models import OrderedItem
from .models import Order, Staff, Receiver

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