from django.shortcuts import render

from items.models import DeliveryReceipt

def filter_view(request):
    qs = DeliveryReceipt.objects.all()
    byItem_query = request.GET.get('search_by_item')
    byItemType_query = request.GET.get('search_by_item_type')
    byDate_query = request.GET.get('search_by_date')
    
    if byItem_query != '':
        qs = qs.filter(title__icontains = byItem_query)

    elif byItemType_query != '':
        qs = qs.filter(title__icontains = byItemType_query)
        
    elif byDate_query != '':
        qs = qs.filter(title__icontains = byDate_query)    
    
    context = {
        'queryset': qs
    }
    return render(request, 'delivery/filter.html', context)


