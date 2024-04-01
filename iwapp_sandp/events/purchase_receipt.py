import frappe
from bs4 import BeautifulSoup

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
            if item.custom_model_id and item.serial_no:
                frappe.db.set_value("Item", item.item_code, "has_serial_no", 1)

def on_submit(doc, method):
    if doc.items:
        for item in doc.items:
            if item.custom_has_serial_no == 1 and item.serial_no:
                frappe.db.set_value("Item Model ID", item.custom_model_id, "serial_no", item.serial_no)
                # Replace commas with newline characters and split the string into a list and Remove spaces from each element in the list
                data_list = [i.strip() for i in item.serial_no.replace(',', '\n').split('\n') if i]
                for i in data_list:
                    frappe.db.set_value("Serial No", i, {"custom_model_id" : item.custom_model_id, "serial_no_details" : item.brand, "brand":item.brand, "custom_update_model_id":1})
