import frappe

def validate(doc, method):
    if doc.items:
        for i in doc.items:
            if i.serial_no:
                data_list = [item.strip() for item in i.serial_no.replace(',', '\n').split('\n') if item]
                if data_list:
                    for serial_no in data_list:
                        model_id = frappe.db.get_value("Serial No", serial_no, "custom_model_id")
                        if model_id:
                            i.custom_model_id = model_id