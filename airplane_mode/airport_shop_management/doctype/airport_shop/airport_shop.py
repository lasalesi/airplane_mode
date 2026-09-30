# Copyright (c) 2026, libracore AG and contributors
# For license information, please see license.txt

import frappe
from frappe.website.website_generator import WebsiteGenerator
import re

class AirportShop(WebsiteGenerator):
    website = frappe._dict(
        template="templates/generators/airport_shop.html",
        condition_field="is_published",
        page_title_field="route",
    )
    
    def get_context(self, context):
        context.no_cache = 1
        
    def before_save(self):
        if not self.route:
            slug = re.sub(r"[^a-z0-9]+", "-", self.name.lower()).strip("-")
            self.route = f"flight/{slug}"
