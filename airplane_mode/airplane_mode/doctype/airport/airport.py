# Copyright (c) 2026, libracore AG and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Airport(Document):
    pass
    
@frappe.whitelist()
def get_shops_summary(airport):
    data = {
        'total_occupied': frappe.db.sql("""
                SELECT IFNULL(COUNT(`name`), 0) AS `count`
                FROM `tabAirport Shop`
                WHERE `available_for_lease` = 0
                  AND `airport` = %(airport)s;
                """, 
                {
                    'airport': airport
                },
                as_dict=True
            )[0]['count'],
        'total_available': frappe.db.sql("""
                SELECT IFNULL(COUNT(`name`), 0) AS `count`
                FROM `tabAirport Shop`
                WHERE `available_for_lease` = 1
                  AND `airport` = %(airport)s;
                """, 
                {
                    'airport': airport
                },
                as_dict=True
            )[0]['count']
    }
    
    html = frappe.render_template("airplane_mode/templates/includes/airport_shop_summary.html", data)
    
    return {
        'html': html
    }
