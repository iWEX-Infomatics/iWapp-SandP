import frappe

def validate(doc, method):
    if doc.items:
        rows_with_missing_model_id = []
        # here i: The current row number, item: The current item being processed in the loop.
        for i, item in enumerate(doc.items, start=1):
            if item.custom_has_model_id == 1 and item.custom_model_id is None:
                rows_with_missing_model_id.append(f"row {i}")
        if rows_with_missing_model_id:
            rows_str = ", ".join(rows_with_missing_model_id)
            frappe.throw(f"Mandatory fields required in Sales Invoice Item for <b>Model ID</b> in <b>{rows_str}.</b>")
        for i in doc.items:
            if i.serial_no:
                data_list = [item.strip() for item in i.serial_no.replace(',', '\n').split('\n') if item]
                if data_list:
                    for serial_no in data_list:
                        model_id_and_brand = frappe.db.get_value("Serial No", serial_no, ["custom_model_id", "brand"])
                        if model_id_and_brand:
                            i.custom_model_id = model_id_and_brand[0]
                            i.brand = model_id_and_brand[1]
def before_save(doc, method):
    if doc.items:
        for item in doc.items:
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