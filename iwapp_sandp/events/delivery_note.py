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
            frappe.throw(f"Mandatory fields required in Delivery Note Item for <b>Model ID</b> in <b>{rows_str}.</b>")
        for i in doc.items:
            if doc.is_return == 1:  # This line checks if the document is a return
                continue  # This line skips the serial number validation for return documents
            if i.custom_model_id:
                if i.custom_has_serial_no == 1:
                    if i.custom_model_wise_serial == 1:
                        serial_no_list = frappe.db.get_list('Serial No',
                            filters={
                                'status': 'Active',
                                'custom_model_id': i.custom_model_id,
                                "warehouse":i.warehouse
                            },
                            order_by='purchase_date asc',
                            pluck = "name"
                        )
                        if serial_no_list:
                            i.serial_no = ""
                            serial_no_list = serial_no_list[:int(i.qty)]
                            serial_no_string = ",".join(serial_no_list)
                            i.serial_no = serial_no_string.replace(',', '\n')
                            if(len(serial_no_list) < i.qty):
                                needed_item = i.qty - len(serial_no_list)
                                frappe.throw(
                                title='Insufficient Stock',
                                msg=f"{needed_item} units of <b><u>Item {i.item_code}</u></b> against <b><u>Model ID {i.custom_model_id}</u></b> needed in <b><u>Warehouse {i.warehouse}</u></b> to complete this transaction.",
                                )
                        else:
                            frappe.throw(
                                title='Insufficient Stock',
                                msg=f"Serial Nos Required for Serialized <b><u>Item {i.item_code}</u></b> against <b><u>Model ID {i.custom_model_id}</u></b>",
                                )
                    else:
                        serial_no_list = frappe.db.get_list('Serial No',
                            filters={
                                'status': 'Active',
                                'custom_model_id': i.custom_model_id,
                                "warehouse":i.warehouse
                            },
                            order_by='purchase_date asc',
                            pluck = "name"
                        )
                        if serial_no_list:
                            dn_serial_no_list = []
                            if i.serial_no:
                                dn_serial_no_list.append(i.serial_no)
                            dn_serial_no_list = dn_serial_no_list[0].split('\n')
                            # Filter elements from list_a that are not in s_list
                            not_in_sno_list = [item for item in dn_serial_no_list if item not in serial_no_list]
                            if not_in_sno_list:
                                frappe.throw(
                                title='Error',
                                msg=f"<b><u>Model ID {i.custom_model_id}</u></b> not belongs to <b>Serial No {not_in_sno_list}</b>"
                            )
                            if(len(serial_no_list) < i.qty):
                                needed_item = i.qty - len(serial_no_list)
                                frappe.throw(
                                title='Insufficient Stock',
                                msg=f"{needed_item} units of <b><u>Item {i.item_code}</u></b> against <b><u>Model ID {i.custom_model_id}</u></b> needed in <b><u>Warehouse {i.warehouse}</u></b> to complete this transaction.",
                            )
                # if i.custom_has_batch_no == 1:
                #     batch_no_list = frappe.db.get_list('Batch',
                #         filters={
                #             'custom_model_id': i.custom_model_id,
                #         },
                #         order_by='manufacturing_date asc',
                #         pluck = "name"
                #     )
                #     if i.batch_no not in batch_no_list:
                #         frappe.throw(
                #         title='Error',
                #         msg=f"<b><u>Model ID {i.custom_model_id}</u></b> not belongs to <b><u>Batch No {i.batch_no}</u></b>"
                #     )
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
            # Initialize custom_from_model_id == 0 will set the brand, specification as in the below
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
