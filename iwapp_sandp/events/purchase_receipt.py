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
            if item.custom_model_id and item.uom != "Nos":
                # To set custom_has_model_id = 1 when creating model id from PR
                item.custom_has_model_id = 1
                item.custom_has_batch_no = 1
                frappe.db.set_value("Item", item.item_code, {"custom_has_model_id" : 1, "has_batch_no" : 1}, update_modified = False)
                # get_list items having BATCH No SERIES BLANK
                model_id_items = frappe.db.get_value("Item", {
                        "name":item.item_code,
                        "batch_number_series": ""}, "name"
                )
                if model_id_items:
                    # Take the first 3 letters from itemcode and with yy-mm-dd and sb set to serial_no_series in ITEM
                    first_three_letters = item.item_code[:3].upper()
                    batch_no_series = f"{first_three_letters}.YY.MM.DD.####"
                    frappe.db.set_value("Item", item.item_code, {"custom_has_model_id" : 1, "has_batch_no" : 1, "create_new_batch" :1,
                    "batch_number_series" : batch_no_series})
            if item.custom_model_id and item.uom == "Nos":
                 # To set custom_has_model_id = 1 when creating model id from PR
                item.custom_has_model_id = 1
                item.custom_has_serial_no = 1
                frappe.db.set_value("Item", item.item_code, {"custom_has_model_id" : 1, "has_serial_no" : 1}, update_modified = False)
                # get_list items having BATCH No SERIES BLANK
                model_id_items = frappe.db.get_value("Item",{
                        "name":item.item_code,
                        "serial_no_series": ""},"name")
                if model_id_items:
                    # Take the first 3 letters from itemcode and with yy-mm-dd and sb set to serial_no_series in ITEM
                    first_three_letters = item.item_code[:3].upper()
                    serial_no_series = f"{first_three_letters}.YY.MM.DD.####"
                    frappe.db.set_value("Item", item.item_code, {"custom_has_model_id" : 1, "has_serial_no" : 1,
                    "serial_no_series" : serial_no_series})
            if item.custom_from_model_id == 0:
                if item.custom_model_id:
                    brand_and_spec = frappe.db.get_value('Item Model ID', item.custom_model_id, ["brand", "specification"])
                    if brand_and_spec:
                        brand = brand_and_spec[0] if brand_and_spec[0] else ""
                        specification = brand_and_spec[1] if brand_and_spec[1] else ""
                        if specification:
                            item.description = f"{item.item_name}, {brand} - {item.custom_model_id}, {specification}"
                        else:
                            item.description = f"{item.item_name}, {brand} - {item.custom_model_id}"
                        item.brand = brand
                        item.custom_from_model_id = 1

def on_submit(doc, method):
    if doc.items:
        for item in doc.items:
            if item.custom_has_serial_no == 1 and item.serial_no:
                frappe.db.set_value("Item Model ID", item.custom_model_id, "serial_no", item.serial_no)
                # Replace commas with newline characters and split the string into a list and Remove spaces from each element in the list
                data_list = [i.strip() for i in item.serial_no.replace(',', '\n').split('\n') if i]
                for i in data_list:
                    frappe.db.set_value("Serial No", i, {"custom_model_id" : item.custom_model_id, "description" : item.description,
                        "brand":item.brand, "custom_update_model_id":1})
            if item.custom_has_batch_no == 1 and item.custom_model_id:
                frappe.db.set_value("Batch", item.batch_no, {"custom_model_id" : item.custom_model_id, "description" : item.description, "custom_brand":item.brand})
                # Replace commas with newline characters and split the string into a list and Remove spaces from each element in the list
                # data_list = [i.strip() for i in item.serial_no.replace(',', '\n').split('\n') if i]
                # for i in data_list:
                    # frappe.db.set_value("Serial No", i, {"custom_model_id" : item.custom_model_id, "description" : item.description, "brand":item.brand, "custom_update_model_id":1})

