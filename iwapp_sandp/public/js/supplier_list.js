frappe.listview_settings['Supplier'] = {
    onload: function(listview) {
        listview.page.add_inner_button(__('Update Accounts'), function() {
            frappe.call({
                "method": "iwapp_sandp.events.supplier.update_account",
                callback: function (r) {
                    // frappe.msgprint("Updated Accounts for all Suppliers")
                }
            })
        });
    }
};