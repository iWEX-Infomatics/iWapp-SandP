import frappe

def before_save(doc, method):
    if doc.custom_item_default == 0:
        if doc.item_defaults:
            doc.item_defaults = []
        custom_default_child = frappe.get_doc('Custom Default Values')
        for i in custom_default_child.item_defaults:
            doc.append("item_defaults", {
                "company": i.get("company"),
                "default_warehouse": i.get("warehouse"),
                "expense_account": i.get("default_expense_account"),
                "income_account": i.get("default_income_account"),
                "default_price_list": i.get("default_price_list"),
                "buying_cost_center": i.get("default_buying_cost_center"),
                "selling_cost_center": i.get("default_selling_cost_center")
            })
        doc.custom_item_default = 1

@frappe.whitelist()
def get_tax_template(tax):
    # custom_default_child = frappe.db.get_doc('Custom Default Values Taxes', fields = ['company', 'abbr', 'tax_category'])
    custom_default_child = frappe.get_doc('Custom Default Values')
    companies = []
    tax_category = []
    for i in custom_default_child.taxes:
        companies.append({"company": (i.get("company"))})
        tax_category.append({"tax_category": (i.get("tax_category"))})
    # set tax_category and company from custom default values as unique
    tax_category_unique = list(set(tax.get('tax_category') for tax in tax_category))
    not_grp_companies = list(set(company.get('company') for company in companies))
    # Use the 'like' operator in the filter
    tax_template = frappe.db.get_list('Item Tax Template', filters={
        'name': ['like', f'GST %{tax}%'],
        'company':['in', not_grp_companies]
    })
    new_list = []
    for template in tax_template:
        for category in tax_category_unique:
            new_list.append({'name': template.get("name"), 'category': category})
    if new_list:
        return new_list