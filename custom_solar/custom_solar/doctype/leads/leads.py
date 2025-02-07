import frappe
from frappe.model.document import Document
import re
 
class Leads(Document):

    def validate(self):
        """Validate mobile number and email format."""
        self.validate_mobile_number()
        self.validate_email()

    def validate_mobile_number(self):
        """Validate mobile number format."""
        if self.mobile_no:
            # Trim leading and trailing spaces
            self.mobile_no = self.mobile_no.strip()

            # If the mobile number doesn't start with a country code (1-3 digits), add the default +91
            if not self.mobile_no.startswith(("+91", "+", "1", "44", "91", "0")):
                # Prepend default +91 and remove leading zeros
                self.mobile_no = "+91 " + self.mobile_no.lstrip("0")
            else:
                # If it has a country code, allow it and remove leading zeros
                self.mobile_no = self.mobile_no.lstrip("0")

            # Regex pattern for the mobile number validation
            pattern = r'^\+?\d{1,3} \d{10}$'

            # If the mobile number doesn't match the expected pattern, raise an error
            if not re.match(pattern, self.mobile_no):
                frappe.throw("Mobile number must follow the format: <Country Code> <10-digit phone number>")

    def validate_email(self):
        """Validate email format."""
        if self.email_id:
            self.email_id = self.email_id.strip()
            
            # Regular expression pattern for email validation
            email_pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'

            if not re.match(email_pattern, self.email_id):
                frappe.throw("Invalid email format. Please enter a valid email address.")

    def on_update(self):
        """Ensure validation happens when the record is updated."""
        self.validate()  # Ensure validation happens on update
 
@frappe.whitelist()
def log_status_change(docname, old_status, new_status, comment):
    """
    Log the status change along with the comment and update the timeline of the lead.
    """
    lead = frappe.get_doc("Leads", docname)
 
    # Create a new comment or log for status change
    activity = frappe.get_doc({
        'doctype': 'Comment',
        'reference_doctype': 'Leads',
        'reference_name': docname,
        'content': f"Status changed from {old_status} to {new_status} by {frappe.session.user}:\n\n> {comment}",
        'comment_type': 'Comment',
        'owner': frappe.session.user,
    })
    activity.insert(ignore_permissions=True)
 
    # Update the Lead's status
    lead.status = new_status
    lead.save()
 
    return {"message": "Status change logged successfully"}
 
@frappe.whitelist()
def get_site_visit_history(lead):
    """
    Get the history of site visits related to the lead.
    """
    # Fetch data related to site visits from custom doctype or any related records
    visits = frappe.get_all('Site_Visit', filters={'lead': lead}, fields=[
        'lead_owner', 'cantilever_position', 'lead', 'shadow_object_analysis',  
        'roof_type', 'structure_type', 'sanction_load', 'is_same_name', 'no_of_floor','final_note','remarks','2d_diagram_of_site','site_image','site_video'
    ])
    
    if not visits:
        return {"message": "No site visits found for this lead"}
    
    return visits
 
 