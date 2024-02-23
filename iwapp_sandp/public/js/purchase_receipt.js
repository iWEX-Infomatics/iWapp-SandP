frappe.ui.form.on('Purchase Receipt', {
    refresh: function (frm) {
        if (frm.doc.docstastus != 1) {
            frm.add_custom_button(__('Create Model Id'), function () {
                if (frm.doc.items) {
                    frm.clear_table("custom_purchase_item_entry")
                    frm.refresh_field("custom_purchase_item_entry")
                    $.each(frm.doc.items, function (idx, item) {
                        if (item.custom_has_model_id == 1) {
                            var child = frm.add_child("custom_purchase_item_entry");
                            child.purchase_item = item.item_code
                            child.item_qty = item.qty
                            child.model_number = item.custom_model_id
                            // child.item_rate = item.rate
                            // child.discount_percentage = item.discount_percentage
                            child.unit = item.uom
                            frm.refresh_fields("custom_purchase_item_entry");
                        }
                    })
                }
            })
        }
        frm.fields_dict['custom_purchase_item_entry'].grid.get_field('model_number').get_query = function (doc, cdt, cdn) {
            var child = locals[cdt][cdn];
            return {
                filters: {
                    'item': child.purchase_item
                }
            };
        };
        frm.fields_dict['items'].grid.get_field('custom_model_id').get_query = function (doc, cdt, cdn) {
            var child = locals[cdt][cdn];
            return {
                filters: {
                    'item': child.item_code
                }
            };
        };
    }
});

frappe.ui.form.on('Purchase Receipt Item', {
    custom_model_id: function (frm, cdt, cdn) {
        let row = locals[cdt][cdn];
        if (row.custom_model_id) {
            frappe.db.get_value('Item Model ID', row.custom_model_id, ['brand', 'specification'])
                .then(r => {
                    let values = r.message;
                    var result = row.item_code + "-" + values.specification + "-" + values.brand + "-" + row.custom_model_id;
                    frappe.model.set_value(row.doctype, row.name, "description", result)
                })
        }
    }
})