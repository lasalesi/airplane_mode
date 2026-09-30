import frappe
from frappe.utils import today


def get_public_shops(start=0):
    # Intentional public projection; tenant and contract details are never exposed.
    shops = frappe.get_all('Airport Shop', 
        filters={'is_published': 1},
        fields=['name', 'shop_name', 'airport', 'shop_number', 'shop_type', 'area',
                'available_for_lease', 'rent_amount', 'currency', 'route'], 
        order_by='airport, shop_number',
        limit_start=start, 
        limit_page_length=50
    )

    return shops
