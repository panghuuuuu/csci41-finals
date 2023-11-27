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
            print(type(receiver)) 
            if OrderedItem.objects.filter(item=item, staff_member=receiver).exists():
                raise forms.ValidationError("Ordered item with this Item already exists for the current staff member.")
            ordered_item = OrderedItem(item=item, order_quantity=order_quantity, staff_member=receiver)
            ordered_item.save()
        return cleaned_data

OrderFormSet = forms.modelformset_factory(OrderedItem, form=OrderedItemForm, extra=1, can_delete=True)

class OrderForm(forms.ModelForm):
    supplier = forms.ModelChoiceField(queryset=Supplier.objects.all(), empty_label=None, required=False)
    ordered_items = OrderFormSet(queryset=OrderedItem.objects.none(), prefix='ordered_items')

    class Meta:
        model = Order
        fields = ['supplier', 'ordered_items']

    def clean_ordered_items(self):
        ordered_items = self.cleaned_data['ordered_items']
        if not ordered_items:
            raise forms.ValidationError("At least one ordered item is required.")
        return ordered_items
