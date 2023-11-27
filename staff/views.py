from django.shortcuts import render, redirect
from items.models import Item, OrderedItem
from supplier.models import Supplier
from .models import Staff, Receiver, Order
from .forms import OrderForm, OrderedItemForm
from decimal import Decimal
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

def login_view(request):
    if request.method == 'POST':
        staff_number = request.POST.get('staff_number')
        try:
            staff = Staff.objects.get(staff_number=staff_number)
            user = User.objects.get(username=str(staff_number))
        except Staff.DoesNotExist:
            user = None

        if user is not None and user.check_password(f"{staff.staff_first_name}12345"):
            login(request, user)
            return redirect('get_items')             
        else:
            messages.error(request, 'Invalid staff number. Please try again.')

    return render(request, 'staff/login.html')

def logout_view(request):
    logout(request)
    return redirect('login_view')

def get_items(request):
    suppliers = Supplier.objects.all()
    selected_supplier = None
    items = None

    supplier_name = request.GET.get('supplier')
    if supplier_name:
        selected_supplier = Supplier.objects.get(pk=supplier_name)
        items = Item.objects.filter(supplier=supplier_name)

    return render(request, 'staff/order.html', {'suppliers': suppliers, 'selected_supplier': selected_supplier, 'items': items})

def fetch_ordered_items(request):
    staff = Staff.objects.get(staff_number=request.user.username)
    receiver = Receiver.objects.get(staff=staff)
    ordered_items = OrderedItem.objects.filter(staff_member=receiver)
    return render(request, 'staff/order/ordered_item.html', {'ordered_items': ordered_items})

def order_item(request):
    suppliers = Supplier.objects.all()

    ordered_items_key = f'ordered_items_{request.user.id}'
    ordered_items = request.session.get(ordered_items_key, [])
    if request.method == 'POST':
        form = OrderedItemForm(request.POST, request=request)
        if form.is_valid():
            selected_item = form.cleaned_data['item']
            selected_quantity = form.cleaned_data['order_quantity']
            selected_supplier = request.POST.get('supplier')
            existing_item = None
            for item_data in ordered_items:
                if item_data['item']['number'] == selected_item.item_number:
                    item_data['order_quantity'] = selected_quantity
                    item_data['total_cost'] = float(selected_item.item_cost) * item_data['order_quantity']
                    existing_item = item_data
                    break
            if existing_item:
                existing_item['order_quantity'] = selected_quantity
                existing_item['total_cost'] = float(selected_item.item_cost) * existing_item['order_quantity']
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
                staff = Staff.objects.get(staff_number=request.user.username)
                receiver = Receiver.objects.get(staff=staff)
                order_instance = Order.objects.create(staff=staff, supplier=selected_supplier)

                order_item_instance = OrderedItem.objects.create(
                    item=selected_item,
                    order_quantity=selected_quantity,
                    staff_member=receiver
                )

                order_instance.ordered_items.add(order_item_instance)

            request.session[ordered_items_key] = ordered_items
        else:
            print(f"Form Errors: {form.errors}")
    else:
        form = OrderedItemForm(request=request)

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
