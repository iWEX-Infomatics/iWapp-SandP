import frappe


def before_save(doc, method):
    if doc.employee:
        default_shift = frappe.db.get_value("Employee", doc.employee, "default_shift")
        if default_shift:
            doc.shift = default_shift