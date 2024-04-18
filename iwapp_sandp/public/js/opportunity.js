frappe.ui.form.on('Opportunity', {
    custom_site_address: function (frm) {
        dislpay_site_address(frm)
        // the below commmented code is for displaying site address in Small Text
        
        // if (frm.doc.custom_site_address) {
        //     // Fetch the Address document based on the custom_site_address field
        //     frappe.db.get_doc('Address', frm.doc.custom_site_address)
        //         .then(doc => {
        //             // Initialize an array to hold the address components
        //             let address_components = [doc.address_line1];

        //             // Always add city
        //             address_components.push(doc.city);

        //             // Check if county and city are the same, ignoring case sensitivity
        //             if (doc.county && doc.city && doc.county.toLowerCase() !== doc.city.toLowerCase()) {
        //                 address_components.push(doc.county);
        //             }

        //             if (doc.state) {
        //                 address_components.push(doc.state);
        //             }

        //             if (doc.country) {
        //                 address_components.push(doc.country);
        //             }

        //             // Add doc.pincode to the address components if it exists, formatted with a dash and a space
        //             if (doc.pincode) {
        //                 address_components.push(`- ${doc.pincode}`);
        //             }

        //             // Join the address components with a comma and space, but leave out the final comma
        //             const site_address_display = address_components.join(', ').replace(/, (?=\-)/, ' ');

        //             // Set the combined string to the custom_site_address_display field
        //             frm.set_value('custom_site_address_display', site_address_display);
        //         });
        // } else {
        //     frm.set_value('custom_site_address_display', '');
        // }
    },
    party_name: function (frm) {
        frm.set_value("custom_site_address", "")
        set_site_address_filter(frm)

    },
    refresh: function (frm) {
        dislpay_site_address(frm)
        set_site_address_filter(frm)
    },
});

var set_site_address_filter = function (frm) {
    if (frm.doc.opportunity_from == "Customer" && frm.doc.party_name) {
        frm.set_query('custom_site_address', function (doc) {
            return {
                filters: {
                    'link_doctype': 'Customer',
                    'link_name': doc.party_name
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
