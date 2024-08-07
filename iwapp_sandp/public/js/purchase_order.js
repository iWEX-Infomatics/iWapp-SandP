frappe.ui.form.on('Purchase Order', {
    custom_site_address: function (frm) {
        dislpay_site_address(frm)
    },
    custom_customer: function (frm) {
        frm.set_value("custom_site_address", "")
        set_site_address_filter(frm)

    },
    refresh: function (frm) {
        dislpay_site_address(frm)
        set_site_address_filter(frm)
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

frappe.ui.form.on('Purchase Order Item', {
    custom_model_id: function (frm, cdt, cdn) {
        var item = locals[cdt][cdn];
        frappe.model.set_value(cdt, cdn, "description", "")
        if (item.custom_model_id) {
            get_last_purchase_rate(frm, item)
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
        if (item.custom_model_id) {
            frappe.model.set_value(cdt, cdn, "custom_model_id", "")
        }
        if (frm.doc.supplier && item.item_code && item.custom_has_model_id == 0) {
            get_last_purchase_rate(frm, item)
        }
    }
});
var set_site_address_filter = function (frm) {
    if (frm.doc.custom_customer) {
        frm.set_query('custom_site_address', function (doc) {
            return {
                filters: {
                    'link_doctype': 'Customer',
                    'link_name': doc.custom_customer
                }
            }
        })
    }
}

var dislpay_site_address = function (frm) {
    if (frm.doc.custom_site_address) {
        // Fetch the Address document based on the custom_site_address field
        frappe.db.get_doc('Address', frm.doc.custom_site_address)
            .then(doc => {
                // Initialize an array to hold the address components
                let address_components = [doc.address_line1];

                // Arlways add city
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
                } r

                // Join the address components with a comma and space, but leave out the final comma
                const site_address_display = address_components.join(', ').replace(/, (?=\-)/, ' ');

                // Set the combined string to the HTML field
                frm.set_df_property('custom_site_address_html', 'options', site_address_display);
            });
    }
}
function get_last_purchase_rate(frm, item) {
    frappe.call({
        method: "iwapp_sandp.events.purchase_order.get_last_purchase_rate",
        args: {
            item_code: item.item_code,
            model_id: item.custom_model_id
        },
        callback: function (r) {
            if (r.message.length > 0) {
                let data = r.message;
                show_rate_dialog(frm, item, data)
            }
        }
    })
}
function show_rate_dialog(frm, item, data) {
    let fields = [{
        fieldname: "rates",
        fieldtype: 'Table',
        cannot_add_rows: true,
        cannot_delete_rows: true,
        in_place_edit: true,
        fields: [
            {
                label: 'Purchase Invoice',
                fieldname: 'name',
                fieldtype: 'Link',
                options: 'Purchase Invoice',
                in_list_view: 1,
                read_only: 1,
                columns: 3
            },
            // {
            //     label: 'Supplier',
            //     fieldname: 'supplier',
            //     fieldtype: 'Link',
            //     options: 'Supplier',
            //     in_list_view: 1,
            //     read_only: 1,
            //     columns: 2
            // },
            {
                label: 'Date',
                fieldname: 'posting_date',
                fieldtype: 'Date',
                in_list_view: 1,
                read_only: 1,
                columns: 2
            },
            {
                label: 'Quantity',
                fieldname: 'qty',
                fieldtype: 'Float',
                in_list_view: 1,
                read_only: 1,
                columns: 2
            },
            {
                label: 'Last Purchase Rate',
                fieldname: 'rate',
                fieldtype: 'Currency',
                in_list_view: 1,
                read_only: 1,
                columns: 3
            },
        ],
        data: data,

    }]
    let d = new frappe.ui.Dialog({
        title: 'Last Purchase Rate of ' + item.item_code,
        size: 'large',
        fields: fields,
        primary_action_label: 'Select',
        primary_action(value) {
            let selected_rate = d.fields_dict.rates.grid.get_selected_children();
            if (selected_rate.length > 1) {
                frappe.throw("You can only select one row for Last Purchase Rate.")
            }
            else {
                frappe.model.set_value(item.doctype, item.name, "rate", selected_rate[0].rate)
            }
            d.hide();
        }
    })
    d.show()
}
