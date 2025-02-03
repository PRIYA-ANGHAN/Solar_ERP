# Copyright (c) 2025, varoon soneji and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Leads(Document):
	pass


@frappe.whitelist(allow_guest=True)
def log_status_change(docname, old_status, new_status, comment):

    lead = frappe.get_doc("Leads", docname)
    
    # Generate the log entry
    user = frappe.session.user
    log_entry = f"-> {user} has changed the status from {old_status} to {new_status}\n | {comment}\n"
    
    # Append the log entry to status_change_log
    if lead.status_change_log:
        lead.status_change_log += log_entry
    else:
        lead.status_change_log = log_entry  

    lead.save()


