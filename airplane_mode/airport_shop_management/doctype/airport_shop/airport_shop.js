// Copyright (c) 2026, libracore AG and contributors
// For license information, please see license.txt

frappe.ui.form.on("Airport Shop", {
    refresh(frm) {
        if (frm.doc.__islocal) {
            // fetch default rent
            frappe.call({
                'method': 'frappe.client.get',
                'args': {
                    'doctype': 'Airport Shop Settings',
                    'name': 'Airport Shop Settings'
                },
                'callback': function(response) {
                    cur_frm.set_value("rent_amount", response.message.default_rent_amount);
                }
            });
        }
        
        // filter for crono based on customer link field
        cur_frm.fields_dict.shop_type.get_query = function(doc) {
             return {
                filters: {
                    "enabled": 1
                }
             }
        }
    }
});
