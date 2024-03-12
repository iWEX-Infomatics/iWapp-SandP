frappe.ui.form.on("Sales Invoice", {
    refresh: function (frm) {
        frm.fields_dict['items'].grid.get_field('custom_model_id').get_query = function (doc, cdt, cdn) {
            var child = locals[cdt][cdn];
            return {
                filters: {
                    'item': child.item_code
                }
            };
        };
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
    }
})