import frappe

def validate(doc, method):
    if doc.items:
        for i in doc.items:
            model_id = frappe.db.get_value("Item", i.item_code, "custom_has_model_id")
            if model_id:
                i.custom_has_model_id = model_id

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

@frappe.whitelist()
def get_last_purchase_rate(supplier, item_code):
    rates = frappe.db.sql("""
                SELECT
                    po.name,
                    po.transaction_date,
                    poi.rate
                FROM
                    `tabPurchase Order` as po JOIN
                    `tabPurchase Order Item` as poi ON
                    poi.parent = po.name
                WHERE
                    po.docstatus = 1 AND poi.item_code = %s AND po.supplier = %s
                ORDER BY
                    po.transaction_date DESC
                LIMIT 5
                          """, (item_code, supplier) , as_dict = 1)

    # by using str.format()
    # rates = frappe.db.sql("""
    #             SELECT
    #                 po.name,
    #                 po.transaction_date,
    #                 poi.rate
    #             FROM
    #                 `tabPurchase Order` as po JOIN
    #                 `tabPurchase Order Item` as poi ON
    #                 poi.parent = po.name
    #             WHERE
    #                 poi.item_code = '{}' AND po.supplier = '{}'
    #             ORDER BY
    #                 po.transaction_date DESC
    #             LIMIT 5
    #           """.format(item_code, supplier), as_dict=1)

    return rates