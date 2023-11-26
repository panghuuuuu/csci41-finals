from django import forms
from django.forms import BaseFormSet
from supplier.models import Supplier
from items.models import OrderedItem
from .models import Order

class OrderedItemForm(forms.ModelForm):
    class Meta:
        model = OrderedItem
        fields = ['item', 'order_quantity']

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
