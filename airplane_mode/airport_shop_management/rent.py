"""
Management file for rent

"""
import frappe
from frappe.utils import cint, getdate

def create_rent_slip(shop):
    new_rent_slip = frappe.new_doc("Rent Slip")
    new_rent_slip.update({
        'shop': shop,
        'posting_date': getdate(),
        'rent_amount': frappe.get_value("Airport Shop", shop, "rent_amount"),
        'is_paid': 0
    })
    new_rent_slip.insert()
    new_rent_slip.submit()
    return new_rent_slip.name

def process_rent():
    # check which shops are due for rent
    create_rent_slips_for = frappe.db.sql("""
        SELECT `name`
        FROM `tabAirport Shop`
        WHERE 
            `available_for_lease` = 0
        ;
        """,
        as_dict=True
    )
    
    for rs in create_rent_slips_for:
        rent_slip = create_rent_slip(rs['name'])
        
        if cint(frappe.get_value("Airport Shop Settings", "Airport Shop Settings", "enable_rent_reminders")):
            recipient = frappe.db.get_value('Airport Shop', rs['name'], 'email')
            frappe.sendmail(
                recipients=[recipient], 
                subject=f'New Rent Slip {rent_slip}',
                message=frappe.render_template('airplane_mode/templates/emails/shop_rent_reminder.html',
                    {'shop': rs['name']}), 
                reference_doctype='Rent Slip', 
                reference_name=rent_slip
            )

    return
