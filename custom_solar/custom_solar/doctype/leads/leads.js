// frappe.ui.form.on('Leads', {
//     onload: function(frm) {

//         if (!frm.doc.status) {
//             frm.old_status = ""; 
//         } else {
//             frm.old_status = frm.doc.status; 
//         }
//         console.log("Initial Status:", frm.old_status);
//     },

//     status: function(frm) {
//         if (frm.doc && frm.doc.status) {
//             const old_status = frm.old_status; 
//             const new_status = frm.doc.status; 

//             if (old_status !== new_status) {
//                 console.log('Status has changed.');
//                 console.log('Old Status:', old_status);
//                 console.log('New Status:', new_status);

//                 frappe.prompt(
//                     {
//                         label: 'Add Comment',
//                         fieldname: 'status_comment',
//                         fieldtype: 'Small Text',
//                         reqd: 1 
//                     },
//                     (values) => {
//                         console.log('Comment added:', values.status_comment);


//                         const content = `Status changed from **${old_status}** to **${new_status}** by ${frappe.session.user}:\n\n> "${values.status_comment}"`;


//                         frappe.call({
//                             method: 'frappe.desk.form.utils.add_comment',
//                             args: {
//                                 reference_doctype: 'Leads',
//                                 reference_name: frm.doc.name,
//                                 content: content,
//                                 comment_by: frappe.session.user,
//                                 comment_email: frappe.session.user 
//                             },
//                             callback: function() {

//                                 frm.refresh(); 


//                                 frm.old_status = new_status;
//                             }
//                         });
//                     },
//                     'Status Change Comment',
//                     'Submit'
//                 );
//             }
//         } else {
//             console.error("frm.doc or status field is undefined.");
//         }
//     }
// });
frappe.ui.form.on('Leads', {
    onload: function(frm) {
        if (!frm.doc.status) {
            frm.old_status = "";
        } else {
            frm.old_status = frm.doc.status;
        }
        console.log("Initial Status:", frm.old_status);

        // Adding the custom tab button directly
        frm.add_custom_button(__('Site Visits'), function() {
            console.log("Fetching Site Visits...");

            // Get Site Visit details associated with this Lead
            frappe.call({
                method: 'frappe.client.get_list',
                args: {
                    doctype: 'Site Visit',
                    filters: {
                        lead: frm.doc.name // Assuming 'lead' is the field linking Site Visit to Leads
                    },
                    fields: ['name', 'site_visit_date', 'status', 'comments'],
                },
                callback: function(response) {
                    const site_visits = response.message;
                    let content = 'Site Visit Details:\n\n';
                    
                    if (site_visits && site_visits.length > 0) {
                        site_visits.forEach(function(visit) {
                            content += `Visit Date: ${visit.site_visit_date}\nStatus: ${visit.status}\nComments: ${visit.comments}\n\n`;
                        });
                    } else {
                        content = 'No site visits recorded for this lead.';
                    }

                    // Show site visit details in a modal or alert box
                    frappe.msgprint(content);
                },
                error: function(err) {
                    console.error("Error fetching site visit details:", err);
                }
            });
        }, __('Actions')); // Adding button to the 'Actions' menu on the form's header
    },

    status: function(frm) {
        if (frm.doc && frm.doc.status) {
            const old_status = frm.old_status;
            const new_status = frm.doc.status;

            if (old_status !== new_status) {
                console.log('Status has changed.');
                console.log('Old Status:', old_status);
                console.log('New Status:', new_status);

                frappe.prompt(
                    {
                        label: 'Add Comment',
                        fieldname: 'status_comment',
                        fieldtype: 'Small Text',
                        reqd: 1
                    },
                    (values) => {
                        console.log('Comment added:', values.status_comment);

                        const content = `Status changed from **${old_status}** to **${new_status}** by ${frappe.session.user}:\n\n> "${values.status_comment}"`;

                        frappe.call({
                            method: 'frappe.desk.form.utils.add_comment',
                            args: {
                                reference_doctype: 'Leads',
                                reference_name: frm.doc.name,
                                content: content,
                                comment_by: frappe.session.user,
                                comment_email: frappe.session.user
                            },
                            callback: function() {
                                frm.refresh();
                                frm.old_status = new_status;
                            }
                        });
                    },
                    'Status Change Comment',
                    'Submit'
                );
            }
        } else {
            console.error("frm.doc or status field is undefined.");
        }
    }
});
