frappe.ui.form.on('Payroll Entry', {
	end_date:function(frm) {
		if (frm.doc.start_date && frm.doc.end_date){
		    frm.set_value("posting_date", frm.doc.end_date)
		}
	}
})