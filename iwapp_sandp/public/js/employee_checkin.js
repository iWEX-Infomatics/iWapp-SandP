frappe.ui.form.on('Employee Checkin', {
    time: function (frm) {
        if (frm.doc.time) {
            var datetimeString = frm.doc.time;
            // Split the datetime string by space
            var parts = datetimeString.split(" ");
            // Extract the date part (the first part)
            var datePart = parts[0];
            frm.set_value("custom_date", datePart);
        }
    },
    refresh: function (frm) {
        frm.add_custom_button("View Location", function () {
            window.open("https://www.google.com/maps/search/?api=1&query=" + frm.doc.custom_location, '_blank');
        });
    }
});
