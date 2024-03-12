// Copyright (c) 2024, Iwex Informatics and contributors
// For license information, please see license.txt

frappe.ui.form.on('Custom Default Values', {
	refresh: function (frm) {
        frm.fields_dict['default_values'].grid.get_field('customer_account').get_query = function (doc, cdt, cdn) {
            var child = locals[cdt][cdn];
            return {
                filters: {
                    'company': child.company,
					'account_currency':child.currency,
					'name':"Debtors" + " - " + child.currency + " - " + child.abbreviation
                }
            };
        };
		frm.fields_dict['default_values'].grid.get_field('supplier_account').get_query = function (doc, cdt, cdn) {
            var child = locals[cdt][cdn];
            return {
                filters: {
                    'company': child.company,
					'account_currency':child.currency,
					'name':"Creditors" + " - " + child.currency + " - " + child.abbreviation
                }
            };
        };
    }
});
