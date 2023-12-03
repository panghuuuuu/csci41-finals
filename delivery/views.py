from django.shortcuts import render
from django.utils.datetime_safe import datetime
from django.db.models import Q
from supplier.models import Delivery
from items.models import DeliveredItem

def filter_view(request):
    qs = Delivery.objects.select_related('order__receiver', 'order__supplier')
    showAll_query = request.GET.get('show_all')
    byDeliveryNumber_query = request.GET.get('search_by_deliverynumber')
    byItemModel_query = request.GET.get('search_by_item_model')
    byItemBrand_query = request.GET.get('search_by_item_brand')
    byItemType_query = request.GET.get('search_by_item_type')
    byDate_query = request.GET.get('search_by_date')
    byReceiver_query = request.GET.get('search_by_receiver')
    bySupplier_query = request.GET.get('search_by_supplier')

    if byItemModel_query and byItemBrand_query:
        try:
            if byItemModel_query and byItemBrand_query:
                qs = qs.filter(
                    Q(delivered_items__ordered_item__item__supplier_item_model__icontains=byItemModel_query) &
                    Q(delivered_items__ordered_item__item__supplier_item_brand__icontains=byItemBrand_query)
                )
                if not qs.exists():
                    raise ValueError()
        except ValueError:
            print("No matching records for this item is found.")

    elif byDeliveryNumber_query:
        try:
            qs = qs.filter(delivery_number = byDeliveryNumber_query)
            if not qs.exists():
                raise ValueError()
        except ValueError:
            print("No matching records for this delivery number is found.")

    elif byItemType_query:
        try: 
            qs = qs.filter(delivered_items__ordered_item__item__supplier_item_type__icontains = byItemType_query)
            if not qs.exists():
                raise ValueError()

        except ValueError:
            print("No matching records for this item type is found.")

        
    elif byDate_query:
        try:
            qs = qs.filter(delivery_date = datetime.strptime(byDate_query, '%b. %d, %Y'))
            if not qs.exists():
                raise ValueError()
        except ValueError:
            print("Invalid format. Enter the date in the format 'Mon. DD, YYYY'.")

# change these to gabi's code for view all inventory (supplier side) AND view delivered items (staff + supplier)
    # elif byReceiver_query:
    #     try:
    #         qs = qs.filter(order__receiver = byReceiver_query)
    #         if not qs.exists():
    #             raise ValueError()
    #     except ValueError:
    #         print("Receiver does not exist.")

    # elif bySupplier_query:
    #     try:
    #         qs = qs.filter(order__supplier = bySupplier_query)
    #         if not qs.exists():
    #             raise ValueError()
    #     except ValueError:
    #         print("Supplier does not exist.")
    
    elif showAll_query:
        pass    
    
    context = {
        'queryset': qs,
        'delivered_items': DeliveredItem.objects.filter(delivery__in=qs)
    }
    return render(request, 'delivery/filter.html', context)


