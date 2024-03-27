frappe.listview_settings['Serial No'] = {
    onload: function(listview) {
        listview.page.add_inner_button(__('Update Model ID'), function() {
            frappe.call({
                "method": "iwapp_sandp.events.serial_no.update_model_id",
                callback: function (r) {
                    // frappe.msgprint("Updated Accounts for all Customers")
                }
            })
        });
    }
};