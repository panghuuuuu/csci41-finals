from django.shortcuts import render, HttpResponse, redirect
from items.models import Item, OrderedItem
from supplier.models import Supplier
from .models import Staff, Receiver, Order
from .forms import OrderedItemForm
from decimal import Decimal
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.template.loader import render_to_string

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
    try:
        order = Order.objects.get(receiver=receiver, isDelivered=False)
        order_number = order.order_number
        ordered_items = order.ordered_items.all()
        return render(request, 'staff/order/ordered_item.html', {'ordered_items': ordered_items, 'order_number': order_number})
    except Order.DoesNotExist:
        print("No existing order found for the given criteria.")
        return HttpResponse("No pending order found for current user.")

def order_item(request):
    if request.method == 'POST':
        form = OrderedItemForm(request.POST, request=request)
        if form.is_valid():
            selected_item = form.cleaned_data['item']
            selected_quantity = form.cleaned_data['order_quantity']
            selected_supplier = selected_item.supplier
            staff = Staff.objects.get(staff_number=request.user.username)
            receiver = Receiver.objects.get(staff=staff)
            existing_item = None
            existing_order = Order.objects.filter(receiver=receiver, isDelivered=False).first()
            total_cost = float(selected_item.item_cost) * selected_quantity
            if existing_order:
                for item in existing_order.ordered_items.all():
                    if selected_item == item:
                        existing_item = item
                        break
                if existing_item:
                    return JsonResponse({'error': 'Ordered item with this Item already exists for the current staff member.'})
                
                order_instance = existing_order
            else:              
                order_instance = Order.objects.create(receiver=receiver, supplier=selected_supplier)
            
            order_item_instance = OrderedItem.objects.create(
                item=selected_item,
                order=order_instance,
                order_quantity=selected_quantity,
                staff_member=receiver,
                order_total_cost=total_cost
            )
            order_instance.ordered_items.add(order_item_instance)
            ordered_items = order_instance.ordered_items.all()
            
            ordered_items_html = render_to_string('staff/order/ordered_item.html', {'ordered_items': ordered_items, 'order_number': order_instance.order_number})
            return JsonResponse({'ordered_items_html': ordered_items_html})
        else:
            form_errors = {'error': str(form.errors)}
            return JsonResponse({'error': 'Ordered item with this Item already exists for the current staff member.'})

    return render(request, 'staff/order/ordered_item.html', {'ordered_items': ordered_items})

def submit_order(request):
    if request.method == 'POST':
        staff = Staff.objects.get(staff_number=request.user.username)
        receiver = Receiver.objects.get(staff=staff)
        try:
            order = Order.objects.get(receiver=receiver, isDelivered=False)
            order_number = order.order_number
            order_supplier = order.supplier
            order_receiver = order.receiver
            ordered_items = order.ordered_items.all()
            order_date = order.order_date
            order_time = order.order_time
        except Order.DoesNotExist:
            print("No existing order found for the given criteria.")
            return HttpResponse("No pending order found for current user.")
    return render(request, 'staff/order/receipt.html', {'order_number': order_number, 'ordered_items': ordered_items, 'order_supplier': order_supplier, 'order_receiver': order_receiver, 'order_date': order_date, 'order_time': order_time})
