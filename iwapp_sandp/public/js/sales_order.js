frappe.ui.form.on("Sales Order",{
    refresh:function(frm){
        frm.fields_dict['items'].grid.get_field('custom_model_id').get_query = function(frm, cdt, cdn){
            var child = locals[cdt][cdn];
            if(child.item_code){
            return{
                filters:{
                    item:child.item_code
                }
            }
        }
        }
    }
})