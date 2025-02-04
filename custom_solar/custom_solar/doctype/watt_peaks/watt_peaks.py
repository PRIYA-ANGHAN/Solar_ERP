# Copyright (c) 2025, varoon soneji and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class WattPeaks(Document):
	pass

@frappe.whitelist()
def update_same_price(new_price, panel_type):
    # Update only records with the same panel_type
    frappe.db.sql("""
        UPDATE `tabWatt Peaks`
        SET panel_price = %s
        WHERE panel_type = %s
    """, (new_price, panel_type))
    
    frappe.db.commit()
    return True
