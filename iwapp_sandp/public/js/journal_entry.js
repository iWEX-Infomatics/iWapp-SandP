frappe.ui.form.on("Journal Entry", {
    refresh: function (frm) {
        frm.fields_dict['accounts'].grid.get_field('custom_site_address').get_query = function (frm, cdt, cdn) {
            var child = locals[cdt][cdn];
            if (child.custom_customer) {
                return {
                    filters: {
                        'link_doctype': 'Customer',
                        'link_name': child.custom_customer
                    }
                }
            }
        }
    }
})
frappe.ui.form.on('Journal Entry Account', {
    custom_customer: function (frm, cdt, cdn) {
        frappe.model.set_value(cdt, cdn, "custom_site_address", "");
    },
    custom_site_address: function (frm, cdt, cdn) {
        var child = locals[cdt][cdn];
        if (child.custom_site_address) {
            // Fetch the Address document based on the custom_site_address field
            frappe.db.get_doc('Address', child.custom_site_address).then(doc => {
                // Initialize an array to hold the address components
                let address_components = [doc.address_line1];

                // Add city
                address_components.push(doc.city);

                // Check if county and city are different, ignoring case sensitivity
                if (doc.county && doc.city && doc.county.toLowerCase() !== doc.city.toLowerCase()) {
                    address_components.push(doc.county);
                }

                // Add state, country, and pincode
                if (doc.state) {
                    address_components.push(doc.state);
                }
                if (doc.country) {
                    address_components.push(doc.country);
                }
                if (doc.pincode) {
                    address_components.push(`- ${doc.pincode}`);
                }

                // Combine the address components with comma and space
                const site_address_display = address_components.join(', ').replace(/, (?=\-)/, ' ');

                // Set the combined string to the child field custom_site_address_html
                frappe.model.set_value(cdt, cdn, "custom_display_site_address", site_address_display);

                // Refresh the child table to reflect the updated value
                frm.fields_dict['accounts'].grid.refresh();
            });
        }
    },
});