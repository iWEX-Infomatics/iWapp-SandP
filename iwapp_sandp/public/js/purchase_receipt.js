frappe.ui.form.on('Purchase Receipt', {
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
        if (frm.doc.docstatus != 1) {
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
                            child.has_serial_no = item.custom_has_serial_no
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
        var item = locals[cdt][cdn];
        frappe.model.set_value(cdt, cdn, "description", "")
        if (item.custom_model_id) {
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
    }
    // custom_model_id: function (frm, cdt, cdn) {
    // let row = locals[cdt][cdn];
    // if (row.custom_model_id) {
    //     frappe.db.get_value('Item Model ID', row.custom_model_id, ['brand', 'specification'])
    //         .then(r => {
    //             let values = r.message;
    //             var result = row.item_name + "-" + values.specification + "-" + values.brand + "-" + row.custom_model_id;
    //             frappe.model.set_value(row.doctype, row.name, "description", result)
    //         })
    // }
    // }
})

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
