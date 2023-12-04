from django.shortcuts import render, HttpResponse
from .forms import SalesItemForm
from .models import Agent,Sales
from staff.models import *
from items.models import IssuedItem, Item, SoldItem
from django.http import JsonResponse
from django.template.loader import render_to_string

# Create your views here.
def get_agents(request):
    agents = Agent.objects.all()
    selected_agent = None

    agent_items = None
    agent = request.GET.get('agent')
    sold_items = []
    invoice = None

    if agent:
        selected_agent = Agent.objects.get(agent_number=agent)
        try:
            agent_batch = Issuance.objects.get(agent=selected_agent).batch_number
            agent_items = IssuedItem.objects.filter(batch_number=agent_batch)
        except Issuance.DoesNotExist:
            return HttpResponse("No issuance found for current user.")
        try:
            sales = Sales.objects.filter(agent=selected_agent).first()
            sold_items = SoldItem.objects.filter(invoice_number=sales)
            invoice = sales.invoice_number
        except Sales.DoesNotExist:
            return HttpResponse("No existing sales found for current user.")
    return render(request, 'sales.html', {'agents': agents, 'selected_agent': selected_agent, 'agent_items': agent_items, 'sold_items': sold_items, 'invoice': invoice})

def input_sales(request):
    sold_items = []
    if request.method == 'POST':
        form = SalesItemForm(request.POST, request=request)
        if form.is_valid():
            sold_item = form.cleaned_data['item']
            selected_quantity = form.cleaned_data['sold_quantity']
            agent = request.POST.get('selected_agent')
            selected_agent = Agent.objects.get(agent_number=agent)
            existing_sales = Sales.objects.filter(agent=selected_agent).first() 
            
            if existing_sales:
                sales = existing_sales
            else: 
                sales = Sales.objects.create(agent=selected_agent)

            item_instance = Item.objects.get(item_number=sold_item.item.item_number)
            agent_batch = Issuance.objects.get(agent=selected_agent).batch_number
            agent_item = IssuedItem.objects.filter(batch_number=agent_batch, item=item_instance).first()       
            sold_item_instance = SoldItem.objects.create(item=agent_item, invoice_number=sales, sold_quantity=selected_quantity)
            
            agent_item.issued_quantity -= selected_quantity
            agent_item.save()

            sold_items = SoldItem.objects.filter(invoice_number=sold_item_instance.invoice_number)
            sold_items_html = render_to_string('sales.html', {'sold_items': sold_items, 'invoice_number': sold_item_instance.invoice_number})
            return JsonResponse({'sold_items_html': sold_items_html})
        else:
            form_errors = {'error': str(form.errors)}
            return JsonResponse(form_errors, status=400)
    return render(request, 'sales.html', {'sold_items': sold_items})

def submit_sales(request):
    if request.method == 'POST':
        try:
            agent = request.POST.get('submit_agent')
            selected_agent = Agent.objects.get(agent_number=agent)
            sales = Sales.objects.filter(agent=selected_agent).first()
            sold_items = SoldItem.objects.filter(invoice_number=sales)
            invoice = sales.invoice_number
            client = selected_agent.client
            sales_date = sales.sales_date
            for item in sold_items.all():
                sales.total_sales += item.total_sales
            sales.save()
            total_sales = sales.total_sales

        except Agent.DoesNotExist:
            return HttpResponse("No pending order found for current user.")
    return render(request, 'receipt.html', {'invoice': invoice, 'selected_agent': selected_agent, 'invoice': invoice, 'client': client, 'sales_date': sales_date, 'total_sales': total_sales, 'sold_items': sold_items})
