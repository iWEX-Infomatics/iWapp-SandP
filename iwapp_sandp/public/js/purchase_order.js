frappe.ui.form.on('Purchase Order', {
    refresh: function (frm) {
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