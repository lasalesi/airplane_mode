# Copyright (c) 2026, libracore AG and contributors
# For license information, please see license.txt

import frappe
from frappe.website.website_generator import WebsiteGenerator


class AirplaneFlight(WebsiteGenerator):
    website = frappe._dict(
        template="templates/generators/airplane_flight.html",
        condition_field="is_published",
        page_title_field="route",
    )
    
    def get_context(self, context):
        context.no_cache = 1
        context.source_code = self.source_airport_code
        context.destination_code = self.destination_airport_code

    def before_save(self):
      if not self.route:
          self.route = f"flight/{self.name}"
          
    def on_submit(self):
        self.status = "Completed"
        return
