frappe.ui.form.on('Address', {
    refresh: function (frm) {
        view_button(frm)
    },
    custom_location: function (frm) {
        view_button(frm)
    }
})
let view_button = function (frm) {
    if (frm.doc.custom_location) {
        frm.add_custom_button(__('View in Map'), function () {
            window.open("https://www.google.com/maps/search/?api=1&query=" + frm.doc.custom_location, '_blank');
        })
    }
}