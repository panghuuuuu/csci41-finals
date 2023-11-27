from django.contrib import admin
from .models import Item, SoldItem, DeliveredItem, IssuedItem, ReturnedItem, BatchInventory, ItemType, OrderedItem

class ItemAdmin(admin.ModelAdmin):
    list_display = ('item_number', 'item_brand', 'item_model', 'item_qty', 'item_type', 'item_cost', 'item_SRP', 'item_total_cost', 'supplier')
    search_fields = ('item_brand', 'item_model', 'item_type')

@admin.register(SoldItem, DeliveredItem, IssuedItem, ReturnedItem, OrderedItem)
class ItemTransactionAdmin(admin.ModelAdmin):
    def get_quantity(self, obj):
        if hasattr(obj, 'sold_quantity'):
            return obj.sold_quantity
        elif hasattr(obj, 'order_quantity'):
            return obj.order_quantity
        elif hasattr(obj, 'delivered_quantity'):
            return obj.delivered_quantity
        elif hasattr(obj, 'issued_quantity'):
            return obj.issued_quantity
        elif hasattr(obj, 'quantity_returned'):
            return obj.quantity_returned
        else:
            return None

    list_display = ('item', 'get_quantity')

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('item')

    get_quantity.short_description = 'Quantity'

class BatchInventoryAdmin(admin.ModelAdmin):
    filter_horizontal = ('batch_inventory',)

class ItemTypeAdmin(admin.ModelAdmin):
    list_display = ('item_id', 'item_type_name', 'discount_rate')

admin.site.register(Item, ItemAdmin)
admin.site.register(BatchInventory, BatchInventoryAdmin)
admin.site.register(ItemType, ItemTypeAdmin)
