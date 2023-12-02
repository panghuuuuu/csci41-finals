from django.contrib import admin
from .models import SupplierItem, Item, SoldItem, DeliveredItem, IssuedItem, ReturnedItem, BatchInventory, ItemType, OrderedItem

class SupplierItemAdmin(admin.ModelAdmin):
    list_display = ('supplier_item_number', 'supplier_item_brand', 'supplier_item_model', 'supplier_item_qty', 'supplier_item_type', 'supplier_item_cost', 'supplier_item_total_cost', 'supplier')
    search_fields = ('supplier_item_brand', 'supplier_item_model', 'supplier_item_type')
class ItemAdmin(admin.ModelAdmin):
    list_display = ('item_number', 'item_brand', 'item_model')

class DeliveredItemAdmin(admin.ModelAdmin):
    list_display = ('ordered_item',)
@admin.register(SoldItem, IssuedItem, ReturnedItem, OrderedItem)
class ItemTransactionAdmin(admin.ModelAdmin):
    def get_quantity(self, obj):
        if hasattr(obj, 'sold_quantity'):
            return obj.sold_quantity
        elif hasattr(obj, 'order_quantity'):
            return obj.order_quantity
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

class ItemTypeAdmin(admin.ModelAdmin):
    list_display = ('item_type', 'item_discount', 'item_client')

admin.site.register(SupplierItem, SupplierItemAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(ItemType, ItemTypeAdmin)
admin.site.register(DeliveredItem, DeliveredItemAdmin)
