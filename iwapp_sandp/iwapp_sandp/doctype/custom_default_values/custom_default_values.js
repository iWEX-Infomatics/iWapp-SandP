// Copyright (c) 2024, Iwex Informatics and contributors
// For license information, please see license.txt

frappe.ui.form.on('Custom Default Values', {
    refresh: function (frm) {
        frm.fields_dict['default_values'].grid.get_field('customer_account').get_query = function (doc, cdt, cdn) {
            var child = locals[cdt][cdn];
            return {
                filters: {
                    'company': child.company,
                    'account_currency': child.currency,
                    'name': "Debtors" + " " + child.currency + " - " + child.abbreviation
                }
            };
        };
        frm.fields_dict['default_values'].grid.get_field('supplier_account').get_query = function (doc, cdt, cdn) {
            var child = locals[cdt][cdn];
            return {
                filters: {
                    'company': child.company,
                    'account_currency': child.currency,
                    'name': "Creditors" + " " + child.currency + " - " + child.abbreviation
                }
            };
        };
        frm.set_query("company", "default_values", function () {
            return {
                filters: {
                    is_group: 0
                }
            };
        })
        frm.set_query("company", "taxes", function () {
            return {
                filters: {
                    is_group: 0
                }
            };
        })
        frm.set_query("company", "item_defaults", function () {
            return {
                filters: {
                    is_group: 0
                }
            };
        })
        frm.fields_dict['item_defaults'].grid.get_field('warehouse').get_query = function (doc, cdt, cdn) {
            var child = locals[cdt][cdn];
            return {
                filters: {
                    'company': child.company,
                    'is_group': 0
                }
            };
        };
        frm.fields_dict['item_defaults'].grid.get_field('default_income_account').get_query = function (doc, cdt, cdn) {
            var child = locals[cdt][cdn];
            return {
                filters: {
                    'company': child.company,
                }
            };
        };
        frm.fields_dict['item_defaults'].grid.get_field('default_expense_account').get_query = function (doc, cdt, cdn) {
            var child = locals[cdt][cdn];
            return {
                filters: {
                    'company': child.company,
                }
            };
        };
    },
});

frappe.ui.form.on('Custom Default Values Child', {
    tax_category: function (frm, cdt, cdn) {
        let row = locals[cdt][cdn];
        if (row.tax_category) {
            const category_list = ["Overseas", "Export"]; // Make category_list a constant
            if (category_list.includes(row.tax_category)) {
                // Corrected set_value function call
                frappe.model.set_value(cdt, cdn, "country", "");
            }
        }
    }
});
