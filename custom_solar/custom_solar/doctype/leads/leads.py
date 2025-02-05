# Copyright (c) 2025, varoon soneji and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import re


class Leads(Document):
    def validate(self):
        # If mobile number is provided
        if self.mobile_no:
            # Trim leading and trailing spaces
            self.mobile_no = self.mobile_no.strip()
 
            # If the mobile number doesn't start with a country code (1-3 digits), add the default +91
            if not self.mobile_no.startswith(("+91", "+", "1", "44", "91", "0")):
                # If it doesn't start with a country code, prepend default +91 and remove any leading zeros
                self.mobile_no = "+91 " + self.mobile_no.lstrip("0")
            else:
                # If it has a country code, we allow any country code with a space
                self.mobile_no = self.mobile_no.lstrip("0")  # Remove leading zeros, if any
 
            # Regular expression to check the country code (1-3 digits) and 10-digit phone number format
            # The country code must be followed by a space and then 10 digits
            pattern = r'^\+?\d{1,3} \d{10}$'
 
            # If the mobile number doesn't match the expected pattern, raise an error
            if not re.match(pattern, self.mobile_no):
                frappe.throw("Mobile number must follow the format: <Country Code> <10-digit phone number>")
    def on_update(self):
        self.validate()  # Ensure validation happens when the record is updated

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


