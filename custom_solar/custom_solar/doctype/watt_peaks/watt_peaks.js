// Copyright (c) 2025, varoon soneji and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Watt Peaks", {
// 	refresh(frm) {

// 	},
// });

frappe.ui.form.on('Watt Peaks', {
    panel_price: function(frm) {
        // Calculate Total Price
        frm.set_value('total_price', frm.doc.watt_peakkw * frm.doc.panel_price);
    },
    
    watt_peakkw: function(frm) {
        // Update Total Price if KW changes
        frm.set_value('total_price', frm.doc.watt_peakkw * frm.doc.panel_price);
    },

    same_price: function(frm) {
        if (frm.doc.same_price && frm.doc.panel_type) {
            frappe.call({
                method: 'custom_solar.custom_solar.doctype.watt_peaks.watt_peaks.update_same_price',
                args: {
                    new_price: frm.doc.panel_price,
                    panel_type: frm.doc.panel_type
                },
                callback: function(response) {
                    if (response.message) {
                        frappe.msgprint(__('Updated price for all records with the same panel type'));
                    }
                }
            });
        } else if (!frm.doc.panel_type) {
            frappe.msgprint(__('Please select a Panel Type to update same price records.'));
        }
    }
});
