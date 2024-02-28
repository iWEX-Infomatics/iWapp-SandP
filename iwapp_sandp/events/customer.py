import frappe


def before_save(doc, method):
    default_doc = frappe.get_doc("Custom Default Values")
    if len(default_doc.default_values) > 0:
        doc.accounts = []
        for i in default_doc.default_values:
            if i.currency == doc.default_currency:
                doc.append("accounts", {
                    "company":i.company,
                    "account":i.customer_account
                })

@frappe.whitelist()
def update_account():
    cust = frappe.db.get_list("Customer", pluck="name")
    for i in cust:
        customer = frappe.get_doc("Customer", i)
        default_doc = frappe.get_doc("Custom Default Values")
        if len(default_doc.default_values) > 0:
            customer.accounts = []
            for d in default_doc.default_values:
                if d.currency == customer.default_currency:
                    customer.append("accounts", {
                        "company": d.company,
                        "account": d.customer_account
                    })
            customer.save()