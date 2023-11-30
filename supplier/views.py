from django.shortcuts import render
from staff.models import Order

# Create your views here.
def get_orders(request):
    orders = Order.objects.all()
    return render(request, 'deliveries.html', {'orders': orders})