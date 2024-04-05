import frappe

def validate(doc, method):
    if doc.locations:
        for i in doc.locations:
            if i.serial_no:
                data_list = [item.strip() for item in i.serial_no.replace(',', '\n').split('\n') if item]
                if data_list:
                    for serial_no in data_list:
                        model_id_and_brand = frappe.db.get_value("Serial No", serial_no, ["custom_model_id", "brand"])
                        if model_id_and_brand:
                            i.custom_model_id = model_id_and_brand[0]
                            i.custom_brand = model_id_and_brand[1]
def before_save(doc, method):
    # if doc.locations:
    #     for i in doc.locations:
    #         if i.custom_model_id and i.custom_brand:
    #             i.description = f"{i.item_code} - {i.custom_brand} {i.custom_model_id}"
    if doc.locations:
        for item in doc.locations:
            if item.custom_from_model_id == 0:
                if item.custom_model_id:
                    brand_and_spec = frappe.db.get_value('Item Model ID', item.custom_model_id, ["brand", "specification"])
                    if brand_and_spec:
                        brand = brand_and_spec[0] if brand_and_spec[0] else ""
                        specification = brand_and_spec[1] if brand_and_spec[1] else ""
                        if specification:
                            item.description = f"{item.item_code} - {brand} {item.custom_model_id} - {specification}"
                        else:
                            item.description = f"{item.item_code} - {brand} {item.custom_model_id}"
                        item.custom_brand = brand
                        item.custom_from_model_id = 1