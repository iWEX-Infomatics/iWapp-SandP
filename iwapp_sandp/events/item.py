import frappe

@frappe.whitelist()
def get_tax_template(tax):
    # Use the 'like' operator in the filter
    tax_template = frappe.db.get_list('Item Tax Template', filters={
        'name': ['like', f'GST %{tax}%']
    })
    print(tax_template)
    tax_category = frappe.db.get_list('Tax Category', pluck = "name")
    new_list = []
    for template in tax_template:
        for category in tax_category:
            new_list.append({'name': template['name'], 'category': category})
    print(new_list)
    if new_list:
        return new_list