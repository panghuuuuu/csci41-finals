from django.shortcuts import render, HttpResponse, redirect
from items.models import SupplierItem, Item, OrderedItem
from supplier.models import Supplier
from .models import Staff, Receiver, Order, Issuance
from .forms import OrderedItemForm, IssuanceItemForm
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
    supplier_items = None

    supplier_name = request.GET.get('supplier')
    if supplier_name:
        selected_supplier = Supplier.objects.get(pk=supplier_name)
        supplier_items = SupplierItem.objects.filter(supplier=supplier_name)

    return render(request, 'staff/order.html', {'suppliers': suppliers, 'selected_supplier': selected_supplier, 'supplier_items': supplier_items})

def fetch_ordered_items(request):
    staff = Staff.objects.get(staff_number=request.user.username)
    receiver = Receiver.objects.get(staff=staff)
    try:
        order = Order.objects.get(receiver=receiver, isDelivered=False)
        order_number = order.order_number
        ordered_items = OrderedItem.objects.filter(order=order)
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
            
            supplier_item = SupplierItem.objects.get(supplier_item_number=selected_item.supplier_item_number)
            staff = Staff.objects.get(staff_number=request.user.username)
            receiver = Receiver.objects.get(staff=staff)
            existing_item = None
            existing_order = Order.objects.filter(receiver=receiver, isDelivered=False).first()

            total_cost = float(supplier_item.supplier_item_cost) * selected_quantity

            if selected_quantity > supplier_item.supplier_item_qty:
                return JsonResponse({'error': 'Inputted quantity is more than supplier\'s inventory.'})
            else:
                supplier_item.supplier_item_qty -= selected_quantity
                supplier_item.save()  
            if existing_order:
                for item in list(OrderedItem.objects.filter(order=existing_order)):
                    if selected_item == item.item:
                        existing_item = item
                        break
                if existing_item:
                    return JsonResponse({'error': 'Ordered with this Item already exists for the current staff member.'})
                
                order_instance = existing_order
            else:
                order_instance = Order.objects.create(receiver=receiver, supplier=selected_supplier)
            
            order_item_instance = OrderedItem.objects.create(
                item=selected_item,
                order=order_instance,
                order_quantity=selected_quantity,
                order_total_cost=total_cost
            )
            ordered_items = OrderedItem.objects.filter(order=order_instance)
            
            ordered_items_html = render_to_string('staff/order/ordered_item.html', {'ordered_items': ordered_items, 'order_number': order_instance.order_number})
            return JsonResponse({'ordered_items_html': ordered_items_html})
        else:
            form_errors = {'error': str(form.errors)}
            print(form_errors)
            return JsonResponse({'error': 'Ordered with this Item already exists for the current staff member.'})

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
            ordered_items= OrderedItem.objects.filter(order=order)            
            order_date = order.order_date
            order_time = order.order_time
        except Order.DoesNotExist:
            print("No existing order found for the given criteria.")
            return HttpResponse("No pending order found for current user.")
    return render(request, 'staff/order/receipt.html', {'order_number': order_number, 'ordered_items': ordered_items, 'order_supplier': order_supplier, 'order_receiver': order_receiver, 'order_date': order_date, 'order_time': order_time})


def issue_item(request):
    if request.method == 'POST':
        form = OrderedItemForm(request.POST, request=request)
        if form.is_valid():
            issued_item = form.cleaned_data['item']
            issued_quantity = form.cleaned_data['issued_quantity']
            issued_SRP = form.cleaned_data['issued_SRP']
            delivered_items = DeliveredItem.objects.filter(ordered_item=issued_item)
            staff = Staff.objects.get(staff_number=request.user.username)
            issuer = Receiver.objects.get(staff=staff)

            existing_issuance = None
            existing_issuance = Issuance.objects.filter(issuer=issuer, active=True).first()

            delivered_quantity = 0

            if not delivered_items.exists():
                return JsonResponse({'error': 'Item does not exist.'})

            for delivered_item in delivered_items:
                delivered_quantity += delivered_item.order_quantity
            
            if issuance_quantity > delivered_quantity:
                return JsonResponse({'error': 'Issued quantity is greater than available quantity.'})
            else:
                delivered_quantity -= issuer.quantity
                



