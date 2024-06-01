	// Copyright (c) 2024, Iwex Informatics and contributors
	// For license information, please see license.txt

	frappe.ui.form.on('Daily Mark Attendance Tool', {
		setup: function (frm) {
			frm.set_indicator_formatter("default_shift", (doc) => {
				if (doc.late_in) {
					return "red";
				}
			});
			frm.set_indicator_formatter("employee", (doc) => {
				if (doc.attendance_marked == 1) {
					return "blue";
				}
			});
		},

		refresh: function (frm, cdt, cdn) {
			frm.fields_dict.attendance_mark.$wrapper.find('.grid-add-row').remove();
			// frm.fields_dict.attendance_mark.$wrapper.find('.btn-open-row').remove();
			// frm.fields_dict.attendance_mark.$wrapper.find('.justify-content-center').remove();
			frm.fields_dict.attendance_mark.$wrapper.find('.sortable-handle').click(function () {
				$(".grid-delete-row").remove();
				$(".grid-insert-row-below").remove();
				$(".grid-insert-row").remove();
				$(".grid-duplicate-row").remove();
				$(".grid-move-row").remove();
				$(".grid-append-row").remove();
			})
			frm.fields_dict.attendance_mark.$wrapper.find('.btn-open-row').click(function () {
				$(".grid-delete-row").remove();
				$(".grid-insert-row-below").remove();
				$(".grid-insert-row").remove();
				$(".grid-duplicate-row").remove();
				$(".grid-move-row").remove();
				$(".grid-append-row").remove();
			})

			color_indicator_heading(frm)
			// Call the function to update the status count
			update_status_summary(frm);
			cur_frm.fields_dict.attendance_mark.$wrapper.find('.grid-body .rows').find(".grid-row").each(function (i, item) {
				let d = locals[cur_frm.fields_dict["attendance_mark"].grid.doctype][$(item).attr('data-name')];
				if (d.hours < 8) {
					// $(item).find('.grid-static-col').css({ 'color': '#FF0000' });
					$(item).find('[data-fieldname="hours"]').css({ 'color': 'red', 'font-weight': 'bold' });

				}
				if (d.status == "Check") {
					// $(item).find('.grid-static-col').css({ 'color': '#FF0000' });
					$(item).find('[data-fieldname="status"]').css({ 'color': 'red', 'font-weight': 'bold' });

				}
			});
			frm.refresh_field('attendance_mark');
		},
		shift: function (frm) {
			frm.clear_table("attendance_mark");
			frm.refresh_field('attendance_mark');
		},
		from_date: function (frm) {
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
								child.attendance_requested = emp.attendance_requested
								child.attendance_marked = emp.attendance_marked
								child.attendance = emp.attendance
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
						mark_att_tool: frm.doc.name
					},
					callback: function (r) {

					}
				})
			}
		}
	})

	function update_status_summary(frm) {
		// Initialize counters for each status
		var present_count = 0;
		var absent_count = 0;
		var employee_count = 0;
		var half_day_count = 0;
		var leave_count = 0;
		var other_count = 0;

		// Count the total number of employees with the given shift and active status
		frappe.db.count('Employee', {
			filters: {
				'default_shift': frm.doc.shift,
				'status': 'Active'
			}
		}).then(count => {
			employee_count = count;

			// Loop through the child table
			$.each(frm.doc.attendance_mark, function (idx, att) {
				if (att.status == "Present") {
					present_count++;
				} else if (att.status == "Absent") {
					absent_count++;
				} else if (att.status == "On Leave") {
					leave_count++;
				} else if (att.status == "Half Day") {
					half_day_count++;
				} else {
					other_count++;
				}
			});
			var other_count_style = other_count > 0 ? 'color: red;' : '';
			var status_html = `
				<div style="text-align: center;">
					<p style="font-size: 16px; display: inline-block;">
						<b>Total Employee - ${employee_count}</b>,&nbsp;&nbsp;&nbsp;
						<b>Total Present - ${present_count}</b>,&nbsp;&nbsp;&nbsp;
						<b>Total Half Day - ${half_day_count}</b>,&nbsp;&nbsp;&nbsp;
						<b>Total Leave - ${leave_count}</b>,&nbsp;&nbsp;&nbsp;
						<b>Total Absent - ${absent_count}</b>,&nbsp;&nbsp;&nbsp;
						<b style="${other_count_style}">Balance - ${other_count}</b>
					</p>
				</div>
			`;

			// Update the custom HTML field
			frm.fields_dict.status_html.$wrapper.html(status_html);
		})
	}
	function color_indicator_heading(frm) {
		var color_indicators = `
			<div style="text-align: center;">
				<p style="font-size: 13px; display: inline-block;">
					Column Icons: in Default Shift 🔴 for Late,&nbsp;&nbsp;&nbsp; in ID 🔵 for Attendance Marked,&nbsp;&nbsp;&nbsp; in Hours 🔴 for <8 Worked Hours
				</p>
			</div>
		`;
		// Update the custom HTML field
		frm.fields_dict.color_html.$wrapper.html(color_indicators);
	}
