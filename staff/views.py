from django.shortcuts import render, HttpResponse, redirect
from items.models import SupplierItem, Item, OrderedItem, IssuedItem, TransferredItem, ItemType
from supplier.models import Supplier
from client.models import Client
from agent.models import Agent
from .models import Staff, Receiver, Issuer, Order, Issuance, BatchInventory, Transfer
from .forms import OrderedItemForm, IssuanceItemForm, TransferItemForm
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
            try:
                Receiver.objects.get(staff=staff)
                return redirect('get_items')
            except Receiver.DoesNotExist:
                try:
                    Issuer.objects.get(staff=staff)
                    return redirect('get_inventory_and_issued_items')
                except Issuer.DoesNotExist:
                    user = None
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

def get_inventory_and_issued_items(request):
    clients = Client.objects.all()
    items = Item.objects.all()
    selected_client = None
    client_agents = None

    client_name = request.GET.get('client')
    if client_name:
        selected_client = Client.objects.get(pk=client_name)
        client_agents = Agent.objects.filter(client=client_name)
    
    staff = Staff.objects.get(staff_number=request.user.username)
    issuer = Issuer.objects.get(staff=staff)

    try:
        issuance = Issuance.objects.filter(issuer=issuer, isActive=True).first()
        if issuance:
            batch_number = issuance.batch_number
            issued_items = IssuedItem.objects.filter(batch_number=batch_number)
        else:
            batch_number = None
            issued_items = []
    except Issuance.DoesNotExist:
        batch_number = None
        issued_items = []

    return render(request, 'staff/issuance.html', {'clients': clients, 'selected_client': selected_client, 'client_agents': client_agents, 'issued_items': issued_items, 'batch_number': batch_number, 'items': items})

def fetch_ordered_items(request):
    staff = Staff.objects.get(staff_number=request.user.username)
    receiver = Receiver.objects.get(staff=staff)
    try:
        order = Order.objects.get(receiver=receiver, isDelivered=False)
        order_number = order.order_number
        ordered_items = OrderedItem.objects.filter(order=order)
        return render(request, 'staff/order/ordered_item.html', {'ordered_items': ordered_items, 'order_number': order_number})
    except Order.DoesNotExist:
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
                    return JsonResponse({'error': 'Order with this Item already exists for the current staff member.'})
                
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
            return JsonResponse(form_errors, status=400)

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
            return HttpResponse("No pending order found for current user.")
    return render(request, 'staff/order/receipt.html', {'order_number': order_number, 'ordered_items': ordered_items, 'order_supplier': order_supplier, 'order_receiver': order_receiver, 'order_date': order_date, 'order_time': order_time})


def issue_item(request):
    if request.method == 'POST':
        form = IssuanceItemForm(request.POST, request=request)
        if form.is_valid():
            issued_item = form.cleaned_data['item']
            issued_quantity = form.cleaned_data['issued_quantity']
            issued_SRP = form.cleaned_data['issued_SRP']
            
            item_instance = Item.objects.filter(item_number=issued_item.item_number).first()
            staff = Staff.objects.get(staff_number=request.user.username)
            issuer = Issuer.objects.get(staff=staff)
            agent = request.headers.get('X-Agent')
            client = request.headers.get('X-Client')

            agent_instance = Agent.objects.get(agent_number=agent)
            client_instance = Client.objects.get(client_name=client)

            existing_item = None
            existing_issuance = Issuance.objects.filter(issuer=issuer, isActive=True).first()

            if not item_instance:
                return JsonResponse({'error': 'Item does not exist.'})

            if issued_quantity > item_instance.item_qty:
                return JsonResponse({'error': 'Issued quantity is greater than available quantity.'})
            else:
                item_instance.item_qty -= issued_quantity
                item_instance.save()
            
            item_type = ItemType.objects.get(item_client=client_instance, item_type=item_instance.item_type)
            if existing_issuance:
                for item in list(IssuedItem.objects.filter(batch_number=existing_issuance.batch_number)):
                    if item.item == issued_item:
                        existing_item = issued_item
                        break
                if existing_item:
                    return JsonResponse({'error': 'Issuance with this Item already exists for the current staff member.'})

                issuance_instance = existing_issuance
            else:
                batch = BatchInventory.objects.create()
                issuance_instance = Issuance.objects.create(issuer=issuer, agent=agent_instance, client=client_instance, batch_number=batch)

            issuance_item_instance = IssuedItem.objects.create(
                item=item_instance, 
                issued_quantity=issued_quantity, 
                batch_number=issuance_instance.batch_number,
                issued_SRP=issued_SRP, 
                item_discount = 0, 
                item_type=item_type
            )

            issued_items = IssuedItem.objects.filter(batch_number=issuance_instance.batch_number)
            issued_items_html = render_to_string('staff/issuance/issued_item.html', {'issued_items': issued_items, 'batch_number': issuance_instance.batch_number})
            return JsonResponse({'issued_items_html': issued_items_html})
        else:
            form_errors = {'error': str(form.errors)}
            return JsonResponse(form_errors, status=400)
    return render(request, 'staff/issuance/issued_item.html', {'issued_items': issued_items})

def submit_issuance(request):
    if request.method == 'POST':
        staff = Staff.objects.get(staff_number=request.user.username)
        issuer = Issuer.objects.get(staff=staff)
        try:
            issuance = Issuance.objects.get(issuer=issuer, isActive=True)
            batch_number = issuance.batch_number
            agent = issuance.agent
            client = issuance.client
            issuer = issuance.issuer
            issued_items= IssuedItem.objects.filter(batch_number=batch_number)            
            issue_date = issuance.issue_date
            issue_time = issuance.issue_time
        except Issuance.DoesNotExist:
            return HttpResponse("No pending issuance form found for current user.")
    return render(request, 'staff/issuance/issuance_form.html', {'batch_number': batch_number, 'agent': agent, 'client': client, 'issuer': issuer, 'issued_items': issued_items, 'issue_date': issue_date, 'issue_time': issue_time})

def fetch_batch_items(request):
    batches = Issuance.objects.all()
    source_batch_number = None
    receiver_batch_number = None
    source_batch = None
    receiver_batch = None
    
    source = request.GET.get('source')
    receiver = request.GET.get('receiver')

    try:
        source_batch_number = source
        source_batch = IssuedItem.objects.filter(batch_number=source)
    except Issuance.DoesNotExist:
        source_batch = None

    try:
        receiver_batch_number = receiver
        receiver_batch = IssuedItem.objects.filter(batch_number=receiver)
    except Issuance.DoesNotExist:
        receiver_batch = None
    try:
        transfer_form = Transfer.objects.get(isComplete=False)
        transferred_items = TransferredItem.objects.filter(transfer_number=transfer_form)
    except Transfer.DoesNotExist:
        transferred_items = []
    return render(request, 'staff/transfer.html', {'source_batch': source_batch, 'receiver_batch': receiver_batch, 'batches': batches, 'receiver_batch_number': receiver_batch_number, 'source_batch_number': source_batch_number, 'transferred_items': transferred_items})


def transfer_items(request):
    if request.method == 'POST':
        form = TransferItemForm(request.POST, request=request)
        if form.is_valid():
            receiver_batch_number = form.cleaned_data['receiver_batch_number']
            source_batch_number = form.cleaned_data['batch_number']
            item = form.cleaned_data['item']

            if IssuedItem.objects.filter(batch_number=receiver_batch_number, item=item).exists():
                return HttpResponse("Cannot transfer item. Existing item already exists in receiving batch.")
            existing_transfer = Transfer.objects.filter(isComplete=False).first()

            try:
                transferred_item = IssuedItem.objects.get(batch_number=source_batch_number, item=item)
            except IssuedItem.DoesNotExist:
                return HttpResponse("No matching issued item found.")

            transferred_item.batch_number = receiver_batch_number
            transferred_item.save()

            if existing_transfer:
                transfer_form = existing_transfer
            else:
                transfer_form = Transfer.objects.create(receiver_batch_number=receiver_batch_number, source_batch_number=source_batch_number)
 
            transferred_item_instance = TransferredItem.objects.create(transfer_number=transfer_form, transferred_item=transferred_item)
            receiver_batch = IssuedItem.objects.filter(batch_number=receiver_batch_number)
            source_batch = IssuedItem.objects.filter(batch_number=source_batch_number)
            transfer_form = Transfer.objects.get(isComplete=False)
            transferred_items = TransferredItem.objects.filter(transfer_number=transfer_form)
            return render(request, 'staff/transfer.html', {'receiver_batch': receiver_batch, 'source_batch': source_batch, 'transferred_items': transferred_items})

        else:
            form_errors = {'error': str(form.errors)}
            return JsonResponse(form_errors, status=400)
            
def complete_transfer(request):
    if request.method == 'POST':
        try:
            transfer_form = Transfer.objects.get(isComplete=False)
            source_batch_number = transfer_form.source_batch_number
            receiver_batch_number = transfer_form.receiver_batch_number
            source = Issuance.objects.get(batch_number=source_batch_number)
            source_agent = source.agent
            receiver = Issuance.objects.get(batch_number=receiver_batch_number)
            receiving_agent = receiver.agent
            transferred_items = TransferredItem.objects.filter(transfer_number=transfer_form)
            transfer_date = transfer_form.transfer_date
            transfer_form.isComplete = True
            transfer_form.save()
        except Transfer.DoesNotExist:
            return HttpResponse("No pending transfer form found.")
    return render(request, 'staff/transfer/transfer_form.html', {'source_batch_number': source_batch_number, 'receiver_batch_number': receiver_batch_number, 'source_agent': source_agent, 'receiving_agent': receiving_agent, 'transferred_items': transferred_items, 'transfer_date': transfer_date})



                