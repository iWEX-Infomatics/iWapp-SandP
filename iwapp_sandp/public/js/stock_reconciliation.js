frappe.ui.form.on('Stock Reconciliation', {
    refresh: function (frm) {
        if (frm.doc.docstatus != 1) {
            frm.add_custom_button(__('Fetch Model Id'), function () {
                if (frm.doc.items) {
                    $.each(frm.doc.items, function (idx, item) {
                        if (item.serial_no) {
                            let dataString = item.serial_no
                            let dataList = dataString.replace(/,/g, '\n').split('\n').map(item => item.trim()).filter(Boolean);
                            $.each(dataList, function (idx, serial_no) {
                                frappe.db.get_value("Serial No", serial_no, 'custom_model_id')
                                    .then(r => {
                                        if (r.message.custom_model_id) {
                                            frappe.model.set_value(item.doctype, item.name, "custom_model_id", r.message.custom_model_id)
                                        }
                                    })
                            })
                        }
                    })
                }
            })
        }
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

frappe.ui.form.on('Stock Reconciliation Item', {
    custom_model_id: function (frm, cdt, cdn) {
        var item = locals[cdt][cdn];
        frappe.model.set_value(cdt, cdn, "custom_description", "")
        if (item.custom_model_id) {
            frappe.db.get_value('Item Model ID', item.custom_model_id, ["brand", "specification"]).then(response => {
                const brand_and_spec = response.message;
                if (brand_and_spec) {
                    const brand = brand_and_spec.brand || "";
                    const specification = brand_and_spec.specification || "";
                    if (specification) {
                        const description = `${item.item_name}, ${brand} - ${item.custom_model_id}, ${specification}`;
                        frappe.model.set_value(cdt, cdn, "custom_description", description)
                    } else {
                        const description = `${item.item_name}, ${brand} - ${item.custom_model_id}`;
                        frappe.model.set_value(cdt, cdn, "custom_description", description)
                    }
                }
            });
        }
    },
    item_code: function (frm, cdt, cdn) {
        var item = locals[cdt][cdn];
        if (item.custom_model_id) {
            frappe.model.set_value(cdt, cdn, "custom_model_id", "")
        }
    }
});