frappe.ui.form.on('Leads', {
    onload: function(frm) {

        if (!frm.doc.status) {
            frm.old_status = ""; 
        } else {
            frm.old_status = frm.doc.status; 
        }
        console.log("Initial Status:", frm.old_status);
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
