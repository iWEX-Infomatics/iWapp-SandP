import frappe

def validate(doc, method):
    if doc.custom_purchase_item_entry:
        for model in doc.custom_purchase_item_entry:
            for item in doc.items:
                if item.item_code ==  model.purchase_item:
                    item.custom_model_id = model.model_number
                    item.qty = model.item_qty
                    # item.rate = model.item_rate
                    # item.discount_percentage = model.discount_percentage
                    item.uom = model.unit
                    item.serial_no = model.serial_number

def before_save(doc, method):
    if doc.items:
        for item in doc.items:
            if item.custom_model_id:
                brand_and_spec = frappe.db.get_value('Item Model ID', item.custom_model_id, ["brand", "specification"])
                if brand_and_spec:
                    brand = brand_and_spec[0] if brand_and_spec[0] else ""
                    specification = brand_and_spec[1] if brand_and_spec[1] else ""
                    item.description = f"{item.item_code}-{specification}-{brand}-{item.custom_model_id}"
                    item.brand = brand