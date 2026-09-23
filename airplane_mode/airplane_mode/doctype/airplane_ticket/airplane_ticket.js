// Copyright (c) 2026, libracore AG and contributors
// For license information, please see license.txt

frappe.ui.form.on("Airplane Ticket", {
    refresh(frm) {
        frm.add_custom_button(__('Assign Seat'), () => {
            frappe.prompt(
                {
                    fieldname: 'seat_number',
                    label: __('Seat Number'),
                    fieldtype: 'Data',
                    reqd: 1
                },
                (values) => {
                    frm.set_value('seat', values.seat_number);
                },
                __('Assign Seat'),
                __('Assign')
            );
        }, __('Actions'));
    },
});
