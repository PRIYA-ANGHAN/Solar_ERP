# import frappe
# from frappe.model.document import Document
# import re
 
# class Leads(Document):
 
#     def validate(self):
#         """Validate mobile number and email format."""
#         self.validate_mobile_number()
#         self.validate_email()
 
#     def validate_mobile_number(self):
#         """Validate mobile number format."""
#         if self.mobile_no:
#             # Trim leading and trailing spaces
#             self.mobile_no = self.mobile_no.strip()
 
#             # If the mobile number doesn't start with a country code (1-3 digits), add the default +91
#             if not self.mobile_no.startswith(("+91", "+", "1", "44", "91", "0")):
#                 # Prepend default +91 and remove leading zeros
#                 self.mobile_no = "+91 " + self.mobile_no.lstrip("0")
#             else:
#                 # If it has a country code, allow it and remove leading zeros
#                 self.mobile_no = self.mobile_no.lstrip("0")
 
#             # Regex pattern for the mobile number validation
#             pattern = r'^\+?\d{1,3} \d{10}$'
 
#             # If the mobile number doesn't match the expected pattern, raise an error
#             if not re.match(pattern, self.mobile_no):
#                 frappe.throw("Mobile number must follow the format: <Country Code> <10-digit phone number>")

#     def validate_email(self):
#         """Validate email format."""
#         if self.email_id:
#             self.email_id = self.email_id.strip()
            
#             # Regular expression pattern for email validation
#             email_pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
 
#             if not re.match(email_pattern, self.email_id):
#                 frappe.throw("Invalid email format. Please enter a valid email address.")
 
# @frappe.whitelist()
# def log_status_change(docname, old_status, new_status, comment):
#     """
#     Log the status change along with the comment and update the timeline of the lead.
#     """
#     lead = frappe.get_doc("Leads", docname)
 
#     # Create a new comment or log for status change
#     activity = frappe.get_doc({
#         'doctype': 'Comment',
#         'reference_doctype': 'Leads',
#         'reference_name': docname,
#         'content': f"Status changed from {old_status} to {new_status} by {frappe.session.user}:\n\n> {comment}",
#         'comment_type': 'Comment',
#         'owner': frappe.session.user,
#     })
#     activity.insert(ignore_permissions=True)
 
#     # Update the Lead's status
#     lead.status = new_status
#     lead.save()
 
#     return {"message": "Status change logged successfully"}
 
# @frappe.whitelist()
# def get_site_visit_history(lead):
#     """
#     Get the history of site visits related to the lead.
#     """
#     # Fetch data related to site visits from custom doctype or any related records
#     visits = frappe.get_all('Site_Visit', filters={'lead': lead}, fields=[
#         'lead_owner', 'cantilever_position', 'lead', 'shadow_object_analysis',  
#         'roof_type', 'structure_type', 'sanction_load', 'is_same_name', 'no_of_floor','final_note','remarks','2d_diagram_of_site','site_image','site_video'
#     ])
    
#     if not visits:
#         return {"message": "No site visits found for this lead"}
    
#     return visits
 
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
 
        # Check if the status is 'Closed' before creating/updating Opportunity
        if self.status == "Closed":
            # Ensure required fields are present in the Lead doc
            required_fields = ['full_name', 'email_id', 'mobile_no', 'date_sgma']
            for field in required_fields:
                if not getattr(self, field):
                    frappe.throw(f"Required field '{field}' is missing to create an Opportunity.")
 
            # Fetch existing Opportunity with the same full name
            existing_opportunity = frappe.get_all(
                'Opportunity',
                filters={'full_name': self.full_name},
                fields=['name', 'email_id', 'mobile_no', 'status'],  
                limit=1
            )       
 
            if existing_opportunity:
                opportunity_name = existing_opportunity[0]['name']
                existing_email = existing_opportunity[0]['email_id']
                existing_mobile = existing_opportunity[0]['mobile_no']
 
                # Update existing Opportunity if mobile or email has changed
                if self.email_id != existing_email or self.mobile_no != existing_mobile:
                    opportunity_doc = frappe.get_doc('Opportunity', opportunity_name)
                    opportunity_doc.email_id = self.email_id
                    opportunity_doc.mobile_no = self.mobile_no
                    opportunity_doc.save(ignore_permissions=True)
                    frappe.db.commit()
                    frappe.msgprint(f"Updated Opportunity: <a href='/app/opportunity/{opportunity_name}'>{opportunity_name}</a> with new details.")
                else:
                    frappe.msgprint(f"Opportunity already exists: <a href='/app/opportunity/{opportunity_name}'>{opportunity_name}</a> with the same details.")
            else:
                try:
                        # Create a new Opportunity if no matching record exists
                    opportunity = frappe.get_doc({
                        'doctype': 'Opportunity',
                        'lead_id': self.name,
                        'full_name': self.full_name,
                        'email_id': self.email_id,
                        'mobile_no': self.mobile_no,
                        'date_sgma': self.date_sgma,
                        'status': 'Closed',
                    })
 
                    opportunity.insert(ignore_permissions=True)
                    frappe.db.commit()
 
                    frappe.msgprint(f"New Opportunity created for lead: {self.full_name}")
 
                except Exception as e:
                    frappe.log_error(frappe.get_traceback(), "Opportunity Creation Failed")
                    frappe.throw(f"Failed to create opportunity: {str(e)}")
 
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
 
 