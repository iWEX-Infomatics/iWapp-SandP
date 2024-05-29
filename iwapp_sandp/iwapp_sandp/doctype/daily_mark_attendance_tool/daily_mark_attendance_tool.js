// Copyright (c) 2024, Iwex Informatics and contributors
// For license information, please see license.txt

frappe.ui.form.on('Daily Mark Attendance Tool', {
	setup: function (frm) {
		frm.set_indicator_formatter("employee", (doc) => {
			if (doc.late_in) {
				return "orange";
			}
		});
	},
	refresh: function (frm, cdt, cdn) {
		cur_frm.fields_dict.attendance_mark.$wrapper.find('.grid-body .rows').find(".grid-row").each(function (i, item) {
			let d = locals[cur_frm.fields_dict["attendance_mark"].grid.doctype][$(item).attr('data-name')];
			if (d.hours < 8) {
				// $(item).find('.grid-static-col').css({ 'color': '#FF0000' });
				$(item).find('[data-fieldname="hours"]').css({ 'color': 'orange' });

			}
		});
		frm.refresh_field('attendance_mark');
	},
	shift:function(frm){
		frm.clear_table("attendance_mark");
		frm.refresh_field('attendance_mark');
	},
	from_date:function(frm){
		frm.clear_table("attendance_mark");
		frm.refresh_field('attendance_mark');
	},
	fetch_employee_checkin: function (frm) {
		frm.clear_table("attendance_mark");
		frm.refresh_fields("attendance_mark");
		if (frm.doc.from_date) {
			frappe.call({
				"method": "iwapp_sandp.iwapp_sandp.doctype.daily_mark_attendance_tool.daily_mark_attendance_tool.get_employee_checkin",
				"args": {
					from_date: frm.doc.from_date,
					shift: frm.doc.shift
					//to_date:frm.doc.to_date
				},
				callback: function (r) {
					if (r.message) {
						frm.clear_table("attendance_mark");
						$.each(r.message, function (i, emp) {
							var child = frm.add_child("attendance_mark");
							child.employee = emp.employee
							child.default_shift = emp.shift
							child.date = emp.date
							child.in = emp.in
							child.out = emp.out
							child.hours = emp.hour
							child.status = emp.status
							child.approved = emp.approved
							child.leave_application = emp.leave_application
							child.work_from = emp.work_from
							child.late_in = emp.late_in
							child.early_out = emp.early_out
							child.employee_checkins = emp.employee_checkins
							frm.refresh_fields("attendance_mark");
						})
						frm.save();

					}
				}
			})
		}
	},
	create_attendance: function (frm) {
		if (frm.doc.attendance_mark) {
			frappe.call({
				method: "iwapp_sandp.iwapp_sandp.doctype.daily_mark_attendance_tool.daily_mark_attendance_tool.mark_daily_attendance",
				args: {
					employee_checkins: frm.doc.name
				},
				callback: function (r) {

				}
			})
		}
	}
})
