import frappe


def before_save(doc, method):
    default_doc = frappe.get_doc("Custom Default Values")
    if len(default_doc.default_values) > 0:
        doc.accounts = []
        for i in default_doc.default_values:
            if i.currency == doc.default_currency and i.tax_category == doc.tax_category:
                doc.append("accounts", {
                    "company":i.company,
                    "account":i.supplier_account
                })

@frappe.whitelist()
def update_account():
    supp = frappe.db.get_list("Supplier", pluck="name")
    for supplier_name in supp:
        supplier = frappe.get_doc("Supplier", supplier_name)
        default_doc = frappe.get_doc("Custom Default Values")
        if len(default_doc.default_values) > 0:
            supplier.accounts = []
            for d in default_doc.default_values:
                if d.currency == supplier.default_currency and d.tax_category == supplier.tax_category:
                    supplier.append("accounts", {
                        "company": d.company,
                        "account": d.customer_account
                    })
            supplier.save()
