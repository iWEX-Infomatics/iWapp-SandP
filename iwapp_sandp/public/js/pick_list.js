frappe.ui.form.on('Pick List', {
    refresh: function (frm) {
        frm.fields_dict['locations'].grid.get_field('custom_model_id').get_query = function (doc, cdt, cdn) {
            var child = locals[cdt][cdn];
            return {
                filters: {
                    'item': child.item_code
                }
            };
        };
    }
});