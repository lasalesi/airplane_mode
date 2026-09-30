import frappe
from frappe.utils import cint
from airplane_mode.airport_shop_management.portal import get_public_shops


def get_context(context):
	context.no_cache = 1
	context.start = max(cint(frappe.form_dict.get('start')), 0)
	shops = get_public_shops(context.start)
	context.has_next = len(shops) > 20
	context.shops = shops[:20]
