frappe.ui.form.on("Sales Order", {
    custom_site_address: function (frm) {
        dislpay_site_address(frm)
    },
    customer: function (frm) {
        frm.set_value("custom_site_address", "")
        set_site_address_filter(frm)
    },
    refresh: function (frm) {
        if (frm.doc.docstatus === 1 && frm.doc.status !== 'Closed') {
            frm.add_custom_button(__('Update Model ID'), () => {
                let data = [];
                let d = new frappe.ui.Dialog({
                    title: 'Update Model ID',
                    fields: [
                        {
                            fieldname: 'items',
                            fieldtype: 'Table',
                            cannot_add_rows: true,
                            is_editable_grid: true,
                            data: [],
                            fields: [
                                {
                                    label: 'No.',
                                    fieldname: 'idx',
                                    fieldtype: 'Int',
                                    read_only: 1,
                                    in_list_view: true,
                                    columns: .1
                                },
                                {
                                    label: 'Item Code',
                                    fieldname: 'item_code',
                                    fieldtype: 'Link',
                                    options: 'Item',
                                    read_only: 1,
                                    in_list_view: true,
                                    columns: 2
                                },
                                {
                                    label: 'Model ID',
                                    fieldname: 'model_id',
                                    fieldtype: 'Link',
                                    options: 'Item Model ID',
                                    in_list_view: true,
                                    columns: 2,
                                    get_query: (doc) => {
                                        let filter_model_id = ""
                                        // taking doc idx
                                        // if it is 1st row it will be 1
                                        const idxs = doc["idx"] - 1;
                                        // get a list of dict and take the dict accordingly to idxs
                                        let dialog_data = d.fields_dict.items.df.data[idxs];
                                        filter_model_id = dialog_data.item_code
                                        return {
                                            filters: {
                                                "item": filter_model_id
                                            }
                                        };
                                    }

                                }
                            ]
                        }
                    ],
                    size: 'small', // small, large, extra-large
                    primary_action_label: 'Add',
                    primary_action(values) {
                        $.each(values.items, function (idx, val) {
                            $.each(frm.doc.items, function (idx, item) {
                                if (item.item_code == val.item_code) {
                                    frappe.model.set_value(item.doctype, item.name, "custom_model_id", val.model_id)
                                    frm.refresh_fields("items");
                                    // frm.save();
                                    // frm.refresh();
                                }
                            })
                        })
                        d.hide();
                        // frm.save();
                        // frm.reload_doc();
                    }
                });

                d.show();
                d.$wrapper.find('.modal-content').css("width", "700px");
                $.each(frm.doc.items, function (k, item) {
                    let sl_no_dict = {
                        'item_code': item.item_code,
                        'model_id': item.custom_model_id,
                    };
                    d.fields_dict.items.df.data.push(sl_no_dict);
                    d.fields_dict.items.grid.refresh();
                    d.fields_dict.items.$wrapper.find('.grid-add-row').remove();
                    d.fields_dict.items.$wrapper.find('.grid-row-check').remove();
                    d.fields_dict.items.$wrapper.find('.btn-open-row').remove();

                })
            });
        }
        dislpay_site_address(frm)
        set_site_address_filter(frm)
        frm.fields_dict['items'].grid.get_field('custom_model_id').get_query = function (frm, cdt, cdn) {
            var child = locals[cdt][cdn];
            if (child.item_code) {
                return {
                    filters: {
                        item: child.item_code
                    }
                }
            }
        }
    },
    // for selecting project type in SO to fetch items to table from Item Master
    // custom_project_type:function(frm){
    //     frm.clear_table("items")
    //     if (frm.doc.custom_project_type){
    //         frappe.call({
    //             method:"iwapp_sandp.events.sales_order.get_items_has_project_type",
    //             args:{
    //                 project_type:frm.doc.custom_project_type
    //             },
    //             callback:function(r){
    //                 if(r.message){
    //                     $.each(r.message, function (idx, item){
    //                         var child = frm.add_child("items");
    //                         child.item_code = item
    //                         frm.refresh_fields("items")
    //                     })
    //                 }
    //             }
    //         })
    //     }
    //     frm.refresh_fields("items")
    // }
})
frappe.ui.form.on('Sales Order Item', {
    custom_model_id: function (frm, cdt, cdn) {
        var item = locals[cdt][cdn];
        frappe.model.set_value(cdt, cdn, "description", "")
        if (item.custom_model_id) {
            frappe.db.count('Serial No', {
                filters: {
                    status: 'Active',
                    warehouse: item.warehouse,
                    item_code: item.item_code,
                    custom_model_id: item.custom_model_id
                }
            })
                .then(count => {
                    if (count) {
                        frappe.msgprint(`${parseFloat(count).toFixed(1)} units of <b><u>Item ${item.item_code}</u></b> with <b><u>Model ID ${item.custom_model_id}</u></b> available in <b><u>Warehouse ${item.warehouse}</u></b>`);
                    }
                    else {
                        frappe.msgprint(`No units of <b><u>Item ${item.item_code}</u></b> with <b><u>Model ID ${item.custom_model_id}</u></b> available in <b><u>Warehouse ${item.warehouse}</u></b>.`);
                    }
                })
            frappe.db.get_value('Item Model ID', item.custom_model_id, ["brand", "specification"]).then(response => {
                const brand_and_spec = response.message;
                if (brand_and_spec) {
                    const brand = brand_and_spec.brand || "";
                    const specification = brand_and_spec.specification || "";
                    if (specification) {
                        const description = `${item.item_name}, ${brand} - ${item.custom_model_id}, ${specification}`;
                        frappe.model.set_value(cdt, cdn, "description", description)
                    } else {
                        const description = `${item.item_name}, ${brand} - ${item.custom_model_id}`;
                        frappe.model.set_value(cdt, cdn, "description", description)
                    }
                }
            });
        }
    },
    item_code: function (frm, cdt, cdn) {
        var item = locals[cdt][cdn];
        fetch_actual_qty(item)
        if (item.custom_model_id) {
            frappe.model.set_value(cdt, cdn, "custom_model_id", "")
        }
    },
    // warehouse:function(frm, cdt, cdn){
    //     var item = locals[cdt][cdn];
    //     fetch_actual_qty(item)
    // },
    qty: function (frm, cdt, cdn) {
        var item = locals[cdt][cdn];
        if (item.item_code && item.qty && item.warehouse) {
            if (item.custom_has_model_id == 0) {
                frappe.db.get_value('Bin', { item_code: item.item_code, warehouse: item.warehouse }, 'actual_qty')
                    .then(r => {
                        if (r.message.actual_qty && r.message.actual_qty < item.qty) {
                            let diff_qty = item.qty - r.message.actual_qty;
                            frappe.msgprint(`${parseFloat(diff_qty).toFixed(1)} units of <b><u>Item ${item.item_code}</u></b> needed in <b><u>Warehouse ${item.warehouse}</u></b> to complete this transaction.`);
                        }
                    });
            }
            else {
                if (item.custom_model_id) {
                    frappe.db.count('Serial No', {
                        filters: {
                            status: 'Active',
                            warehouse: item.warehouse,
                            item_code: item.item_code,
                            custom_model_id: item.custom_model_id
                        }
                    })
                        .then(count => {
                            if (count && count < item.qty) {
                                let diff_qty = item.qty - count
                                frappe.msgprint(`${parseFloat(diff_qty).toFixed(1)} units of <b><u>Item ${item.item_code}</u></b> <b><u>Model ID ${item.custom_model_id}</u></b> needed in <b><u>Warehouse ${item.warehouse}</u></b> to complete this transaction.`);
                            }
                        })
                }
            }
        }
    }

});
var set_site_address_filter = function (frm) {
    if (frm.doc.customer) {
        frm.set_query('custom_site_address', function (doc) {
            return {
                filters: {
                    'link_doctype': 'Customer',
                    'link_name': doc.customer
                }
            }
        })
    }
}
// get_doc Address and set the values to a html field
var dislpay_site_address = function (frm) {
    if (frm.doc.custom_site_address) {
        // Fetch the Address document based on the custom_site_address field
        frappe.db.get_doc('Address', frm.doc.custom_site_address)
            .then(doc => {
                // Initialize an array to hold the address components
                let address_components = [doc.address_line1];

                // Always add city
                address_components.push(doc.city);

                // Check if county and city are the same, ignoring case sensitivity
                if (doc.county && doc.city && doc.county.toLowerCase() !== doc.city.toLowerCase()) {
                    address_components.push(doc.county);
                }

                if (doc.state) {
                    address_components.push(doc.state);
                }

                if (doc.country) {
                    address_components.push(doc.country);
                }

                // Add doc.pincode to the address components if it exists, formatted with a dash and a space
                if (doc.pincode) {
                    address_components.push(`- ${doc.pincode}`);
                }

                // Join the address components with a comma and space, but leave out the final comma
                const site_address_display = address_components.join(', ').replace(/, (?=\-)/, ' ');

                // Set the combined string to the HTML field
                frm.set_df_property('custom_site_address_html', 'options', site_address_display);
            });
    }
}

function fetch_actual_qty(item) {
    if (item.item_code && item.warehouse) {
        if (item.custom_has_model_id == 0) {
            frappe.db.get_value('Bin', { item_code: item.item_code, warehouse: item.warehouse }, 'actual_qty')
                .then(r => {
                    if (r.message.actual_qty) {
                        frappe.msgprint(`${parseFloat(r.message.actual_qty).toFixed(1)} units of <b><u>Item ${item.item_code}</u></b> available in <b><u>Warehouse ${item.warehouse}</u></b>`);
                    }
                    else {
                        frappe.msgprint(`No units of <b><u>Item ${item.item_code}</u></b> available in <b><u>Warehouse ${item.warehouse}</u></b>.`);
                    }
                })
        }
    }

}
