import frappe

def validate(doc, method):
    if doc.items:
        for i in doc.items:
            model_id = frappe.db.get_value("Item", i.item_code, "custom_has_model_id")
            if model_id:
                i.custom_has_model_id = model_id