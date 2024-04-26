import frappe

def validate(doc, method):
    if doc.items:
        for i in doc.items:
            if i.custom_model_id:
                serial_no_list = frappe.db.get_list('Serial No',
                    filters={
                        'status': 'Active',
                        'custom_model_id': i.custom_model_id
                    },
                    order_by='purchase_date asc',
                    pluck = "name"
                )
                # Limiting the length of the list to 2
                serial_no_list = serial_no_list[:int(i.qty)]
                serial_no_string = ",".join(serial_no_list)
                i.serial_no = serial_no_string.replace(',', '\n')
                if(len(serial_no_list) < i.qty):
                    needed_item = i.qty - len(serial_no_list)
                    frappe.throw(
                    title='Insufficient Stock',
                    msg=f"{needed_item} units of <b><u>Item {i.item_code}</u></b> against <b><u>Model ID {i.custom_model_id}</u></b> needed in <b><u>Warehouse {i.warehouse}</u></b> to complete this transaction.",
                )
            if i.serial_no and not i.custom_model_id:
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