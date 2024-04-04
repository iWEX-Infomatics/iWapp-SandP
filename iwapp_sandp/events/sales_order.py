import frappe

def validate(doc, method):
    if doc.items:
        for i in doc.items:
            if i.custom_model_id and i.brand:
                i.description = f"{i.item_code} {i.brand} {i.custom_model_id}"
