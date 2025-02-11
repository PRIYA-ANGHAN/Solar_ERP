// Copyright (c) 2025, varoon soneji and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Opportunity", {
// 	refresh(frm) {

// 	},
// });


// Copyright (c) 2025, Varoon Soneji and contributors
// For license information, please see license.txt




frappe.ui.form.on("Opportunity", {
    refresh: function (frm) {
        frm.timeline.wrapper.hide(); // Hides the Activity section
    }
});



