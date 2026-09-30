// Copyright (c) 2026, libracore AG and contributors
// For license information, please see license.txt

frappe.ui.form.on("Airport", {
    refresh(frm) {
        if (!frm.doc.__islocal) {
            show_shop_summary(frm);
        }
    }
});

function show_shop_summary(frm) {
    frappe.call({
        'method': 'airplane_mode.airplane_mode.doctype.airport.airport.get_shops_summary',
        'args': {
            'airport': frm.doc.name
        },
        'callback': function(response) {
            console.log(response.message.html);
            cur_frm.set_df_property('shops_html', 'options', response.message.html);
        }
    });
        
}
