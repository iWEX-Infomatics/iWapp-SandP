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
            frappe.throw(f"Mandatory fields required in Purchase Invoice Item for <b>Model ID</b> in <b>{rows_str}.</b>")