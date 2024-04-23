import frappe

def validate(doc, method):
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
# @frappe.whitelist()
# def get_items_has_project_type(project_type):
#     item = frappe.db.get_list('Project Child',
#         filters={
#             'project_type': ["in", project_type]
#         },
#         pluck = "parent"
#     )
#     if item:
#         return item