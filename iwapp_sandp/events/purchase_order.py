import frappe

def validate(doc, method):
    if doc.items:
        for i in doc.items:
            model_id = frappe.db.get_value("Item", i.item_code, "custom_has_model_id")
            if model_id:
                i.custom_has_model_id = model_id

def before_save(doc, method):
    if doc.items:
        for i in doc.items:
            if i.custom_model_id and i.brand:
                i.description = f"{i.item_code} {i.brand} {i.custom_model_id}"