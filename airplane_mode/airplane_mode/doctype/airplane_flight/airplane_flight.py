# Copyright (c) 2026, libracore AG and contributors
# For license information, please see license.txt

import frappe
from frappe.website.website_generator import WebsiteGenerator
import re

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
            slug = re.sub(r"[^a-z0-9]+", "-", self.name.lower()).strip("-")
            self.route = f"flight/{slug}"
        
    def on_submit(self):
        self.status = "Completed"
        return

    def on_update(self):
        frappe.enqueue(method=async_update_gate, queue='short', timeout=30,
            **{'flight': self.name, 'gate': self.gate})
        return
        
def async_update_gate(flight, gate):
    # update related tickets with the gate number
    frappe.db.sql("""
        UPDATE `tabAirplane Ticket`
        SET `gate` = %(gate)s
        WHERE
            `flight` = %(flight)s;
        """,
        {
            'gate': gate,
            'flight': flight
        }
    )
    frappe.db.commit()
    return
