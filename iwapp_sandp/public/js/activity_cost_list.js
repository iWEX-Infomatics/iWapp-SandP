frappe.listview_settings['Activity Cost'] = {
    onload: function(listview) {
        listview.page.add_inner_button(__('Update Activity Cost'), function() {
            frappe.call({
                "method": "iwapp_sandp.events.activity_cost.update_activity_cost",
                callback: function (r) {
                }
            })
        });
    }
};