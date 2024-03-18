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
                    'name': "Debtors" + " " + child.currency + "- " + child.abbreviation
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
    },
    custom_item_tax_percentage:function(frm){
        frm.clear_table("taxes")
        frm.refresh_field("taxes")
        if(frm.doc.custom_item_tax_percentage){
            frappe.call({
                method:"iwapp_sandp.events.item.get_tax_template",
                args:{
                    tax:frm.doc.custom_item_tax_percentage
                },
                callback:function(r){
                    if(r.message){
                        $.each(r.message, function(idx, tax){
                            let child = frm.add_child("taxes");
                            child.item_tax_template = tax.name
                            child.tax_category = tax.category
                            frm.refresh_fields("taxes");
                        })
                    }
                }
            })
        }
    }
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
