import frappe

def validate(doc, method):
    if doc.items:
        for i in doc.items:
            if i.custom_model_id:
                i.custom_brand = frappe.db.get_value("Item Model ID", i.custom_model_id, "brand")
def on_submit(doc, method):
    if doc.items:
        for item in doc.items:
            if item.serial_no:
                frappe.db.set_value("Item Model ID", item.custom_model_id, "serial_no", item.serial_no)
                # Replace commas with newline characters and split the string into a list and Remove spaces from each element in the list
                data_list = [i.strip() for i in item.serial_no.replace(',', '\n').split('\n') if i]
                for i in data_list:
                    frappe.db.set_value("Serial No", i, {"custom_model_id" : item.custom_model_id, "brand":item.custom_brand, "serial_no_details" : item.custom_brand, "custom_update_model_id":1})
