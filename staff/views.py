from django.shortcuts import render, redirect
from items.models import Item, OrderedItem
from supplier.models import Supplier
from .models import Order
from .forms import OrderForm, OrderedItemForm
from decimal import Decimal

def select_staff(request):
    staff_members = Staff.objects.all()
    return render(request, 'order.html', {'staff_members': staff_members})


def get_items(request):
    suppliers = Supplier.objects.all()
    selected_supplier = None
    items = None

    supplier_name = request.GET.get('supplier')
    if supplier_name:
        selected_supplier = Supplier.objects.get(pk=supplier_name)
        items = Item.objects.filter(supplier=supplier_name)

    return render(request, 'staff/order.html', {'suppliers': suppliers, 'selected_supplier': selected_supplier, 'items': items})

def order_item(request):
    suppliers = Supplier.objects.all()
    form = OrderForm()

    ordered_items = request.session.get('ordered_items', [])
    if request.method == 'POST':
        form = OrderedItemForm(request.POST)
        if form.is_valid():
            selected_item = form.cleaned_data['item']
            selected_quantity = form.cleaned_data['order_quantity']

            for item_data in ordered_items:
                if item_data['item']['number'] == selected_item.item_number:
                    item_data['order_quantity'] = selected_quantity
                    item_data['total_cost'] = float(selected_item.item_cost) * item_data['order_quantity']
                    break
            else:
                total_cost = float(selected_item.item_cost) * selected_quantity
                ordered_items.append({
                    'item': {
                        'number': selected_item.item_number,
                        'brand': selected_item.item_brand,
                        'model': selected_item.item_model,
                    },
                    'order_quantity': selected_quantity,
                    'total_cost': total_cost,
                })
            order_item_instance = OrderItem.objects.create(
                item=selected_item,
                order_quantity=selected_quantity
                )
            request.session['ordered_items'] = ordered_items
        else:
            print(f"Form Errors: {form.errors}")

    return render(request, 'staff/order/ordered_item.html', {'ordered_items': ordered_items})

def submit_order(request):
    if request.method == 'POST':
            staff_member = orm.cleaned_data['staff_member']

            order = Order(staff=staff_member)
            order.save()
            ordered_items = request.session.get('ordered_items', [])
            order.ordered_items.set(ordered_items)

            request.session.pop('ordered_items', None)
            return redirect('success_page')
    return render(request, 'staff/order.html')
