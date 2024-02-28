import frappe


def before_save(doc, method):
    default_doc = frappe.get_doc("Custom Default Values")
    if len(default_doc.default_values) > 0:
        doc.accounts = []
        for i in default_doc.default_values:
            if i.currency == doc.default_currency:
                doc.append("accounts", {
                    "company":i.company,
                    "account":i.supplier_account
                })

@frappe.whitelist()
def update_account():
    supp = frappe.db.get_list("Supplier", pluck="name")
    for i in supp:
        supplier = frappe.get_doc("Supplier", i)
        default_doc = frappe.get_doc("Custom Default Values")
        if len(default_doc.default_values) > 0:
            supplier.accounts = []
            for d in default_doc.default_values:
                if d.currency == supplier.default_currency:
                    supplier.append("accounts", {
                        "company": d.company,
                        "account": d.customer_account
                    })
            supplier.save()