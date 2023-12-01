from django.shortcuts import render, HttpResponse
from staff.models import Order
from .models import Delivery, Supplier
from items.models import Item, DeliveredItem

def get_orders(request):
    orders = Order.objects.filter(isDelivered=False)
    return render(request, 'deliveries.html', {'orders': orders})

def mark_delivered(request):
    if request.method == 'POST':
        order_number = request.POST.get('order_number')
        try:
            order = Order.objects.get(order_number=order_number)
            ordered_items = order.ordered_items.all()
            delivery_instance = Delivery.objects.create(order=order)
            for order_item in ordered_items:
                delivered_item = DeliveredItem.objects.create(order=order_item)
                delivery_instance.delivered_items.add(delivered_item)
            delivery_number = delivery_instance.delivery_number
            delivery_supplier = delivery_instance.order.supplier
            delivery_receiver = delivery_instance.order.receiver
            delivered_items = delivery_instance.delivered_items.all()
            delivery_date = delivery_instance.delivery_date
            delivery_time = delivery_instance.delivery_time
            order.isDelivered = True
            order.save()
        except Order.DoesNotExist:
            print("Order number does not exist.")
            return HttpResponse("No valid order number is found.")
    return render(request, 'deliveryreceipt.html', {'delivery_number': delivery_number, 'delivery_supplier': delivery_supplier, 'delivery_receiver': delivery_receiver, 'delivered_items': delivered_items, 'delivery_date': delivery_date, 'delivery_time': delivery_time})

def get_supplier_inventory(request):
    suppliers = Supplier.objects.all()
    selected_supplier = None
    items = None

    supplier_name = request.GET.get('supplier')
    if supplier_name:
        selected_supplier = Supplier.objects.get(pk=supplier_name)
        items = Item.objects.filter(supplier=supplier_name)

    return render(request, 'allinventory.html', {'suppliers': suppliers, 'selected_supplier': selected_supplier, 'items': items})