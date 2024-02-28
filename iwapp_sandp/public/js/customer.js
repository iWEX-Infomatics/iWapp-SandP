frappe.ui.form.on('Customer', {
    default_currency: function (frm) {
        frm.set_value("default_price_list", "")
        if (frm.doc.default_currency) {
            frappe.db.get_doc('Custom Default Values')
                .then(doc => {
                    if (doc.default_values.length > 0) {
                        $.each(doc.default_values, function (idx, price) {
                            if (frm.doc.default_currency == price.currency) {
                                frm.set_value("default_price_list", price.price_list)
                            }
                        })
                    }
                })
        }
    }
})
