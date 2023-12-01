from django.shortcuts import render, HttpResponse
from staff.models import Order
from .models import Delivery

def get_orders(request):
    orders = Order.objects.all()
    return render(request, 'deliveries.html', {'orders': orders})

def mark_delivered(request):
    if request.method == 'POST':
        order_number = request.POST.get('order_number')
        try:
            order = Order.objects.get(order_number=order_number)
            ordered_items = order.ordered_items.all()
            delivery_instance = Delivery.objects.create(order=order)
            delivery_instance.delivered_items.set(ordered_items)
            delivery_number = delivery_instance.delivery_number
            delivery_supplier = delivery_instance.order.supplier
            delivery_receiver = delivery_instance.order.receiver
            delivered_items = delivery_instance.delivered_items.all()
            delivery_date = delivery_instance.delivery_date
            delivery_time = delivery_instance.delivery_time
        except Order.DoesNotExist:
            print("Order number does not exist.")
            return HttpResponse("No valid order number is found.")
    return render(request, 'deliveryreceipt.html', {'delivery_number': delivery_number, 'delivery_supplier': delivery_supplier, 'delivery_receiver': delivery_receiver, 'delivered_items': delivered_items, 'delivery_date': delivery_date, 'delivery_time': delivery_time})
