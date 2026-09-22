import frappe

def execute():
    print("Populating seats...")

    frappe.reload_doc("Airplane Mode", "doctype", "Airplane Ticket")

    tickets_without_seat = frappe.db.sql("""
        SELECT `name`
        FROM `tabAirplane Ticket`
        WHERE `seat` IS NULL;
        """,
        as_dict=True
    )
    
    for t in tickets_without_seat:
        ticket = frappe.get_doc("Airplane Ticket", t['name'])
        ticket.save()
        

    return
