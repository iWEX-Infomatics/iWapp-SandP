import frappe

def before_save(doc, method):
    if doc.purchase_document_type and doc.purchase_document_no:
        serial_creation_doc = frappe.get_doc(doc.purchase_document_type, doc.purchase_document_no)
        serial_title = doc.serial_no
        if serial_creation_doc:
            for s_no in serial_creation_doc.items:
                if doc.item_code == s_no.item_code:
                    seril_no_list = [item.strip() for item in s_no.serial_no.replace(',', '\n').split('\n') if item]
                    if seril_no_list:
                        # Convert serial_no to lowercase fo comparing serial_no
                        serial_no_lower = serial_title.lower()
                        # Convert each element in list seril_no_list to lowercase and check if serial_no is in it
                        if serial_no_lower in [item.lower() for item in seril_no_list]:
                            if s_no.custom_model_id:
                                doc.custom_model_id = s_no.custom_model_id
                                doc.brand = frappe.db.get_value("Item Model ID", s_no.custom_model_id, "brand")

@frappe.whitelist()
def update_model_id():
    serial_no_list = frappe.db.get_list("Serial No", {"custom_update_model_id": 0, "status": "Active"}, pluck="name")
    updated_count = 0  # Initialize a counter for updated serial numbers
    for s_no in serial_no_list:
        serial_no = frappe.get_doc("Serial No", s_no)  # Retrieve the serial number document
        serial_no.custom_update_model_id = 1  # Update the custom_update_model_id field
        serial_no.save()  # Save the changes
        updated_count = updated_count + 1  # Increment the counter for each updated serial number
    frappe.msgprint(f"Updated {updated_count} serial numbers")  # Print the count of updated serial numbers
