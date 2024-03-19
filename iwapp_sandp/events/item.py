import frappe

@frappe.whitelist()
def get_tax_template(tax):
    custom_default_child = frappe.db.get_list('Custom Default Values Taxes', fields = ['company', 'abbr', 'tax_category'])
    companies = []
    tax_category = []
    for i in custom_default_child:
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