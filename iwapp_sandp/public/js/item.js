frappe.ui.form.on("Item", {
    refresh:function(frm){
        // your code here
    },
    // custom_item_tax_percentage:function(frm){
    //     frm.clear_table("taxes")
    //     frm.refresh_field("taxes")
    //     if(frm.doc.custom_item_tax_percentage){
    //         frappe.call({
    //             method:"iwapp_sandp.events.item.get_tax_template",
    //             args:{
    //                 tax:frm.doc.custom_item_tax_percentage
    //             },
    //             callback:function(r){
    //                 if(r.message){
    //                     $.each(r.message, function(idx, tax){
    //                         let child = frm.add_child("taxes");
    //                         child.item_tax_template = tax.name
    //                         child.tax_category = tax.category
    //                         frm.refresh_fields("taxes");
    //                     })
    //                 }
    //             }
    //         })
    //     }
    // }
})