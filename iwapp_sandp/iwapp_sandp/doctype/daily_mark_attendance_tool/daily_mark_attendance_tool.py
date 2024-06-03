# Copyright (c) 2024, Iwex Informatics and contributors
# For license information, please see license.txt

import frappe, json, datetime
from frappe.model.document import Document

class DailyMarkAttendanceTool(Document):
	pass
@frappe.whitelist()
def get_employee_checkin(from_date, shift):
	if shift == "Shift C (22:30 - 7)":
		to_date = frappe.utils.add_days(from_date, 1)
		# Execute SQL query to retrieve employee check-ins between the specified dates
		# Get check-in records from the database
		checkin_records = frappe.db.sql("""
			SELECT
				ec.name as id,
				ec.employee as employee,
				ec.custom_date as date,
				ec.log_type as log_type,
				ec.shift as shift_type,
				MIN(ec.time) as checkin
			FROM 
				`tabEmployee Checkin` AS ec
			WHERE 
				ec.docstatus = "0" AND
				ec.shift = %s AND
				ec.custom_date BETWEEN %s AND %s
			GROUP BY
				ec.employee, ec.custom_date, ec.log_type
			""", (shift, from_date, to_date), as_dict=True)
		
		# Manual grouping by employee and shift_type
		grouped_records = {}
		for record in checkin_records:
			employee = record["employee"]
			shift_type = record["shift_type"]
			# if employee not in grouped_records: checks if the employee is already a key in grouped_records. 
			# If not, it initializes an empty dictionary for this employee.
			if employee not in grouped_records:
				grouped_records[employee] = {}
			# if shift_type not in grouped_records[employee]: checks if the shift_type is already a key within the employee's dictionary. 
			# If not, it initializes an empty list for this shift type.
			if shift_type not in grouped_records[employee]:
				grouped_records[employee][shift_type] = []
			# grouped_records[employee][shift_type].append(record) appends the current record to the list
			# corresponding to the specific employee and shift type.
			grouped_records[employee][shift_type].append(record)

		# Function to parse datetime string using frappe.utils.get_datetime
		def parse_checkin(record):
			return frappe.utils.get_datetime(record["checkin"])
		aggregated_checkins_list = []
		# Process records for each employee and shift
		for employee, shifts in grouped_records.items():
			for shift_type, records in shifts.items():
				# Filter IN and OUT records based on date
				in_records = [rec for rec in records if rec["log_type"] == "IN" and rec['date'].strftime('%Y-%m-%d') == from_date]
				out_records = [rec for rec in records if rec["log_type"] == "OUT" and rec['date'].strftime('%Y-%m-%d') == to_date]

				# Find earliest IN record and latest OUT record
				earliest_in_record = min(in_records, key=parse_checkin) if in_records else None
				latest_out_record = max(out_records, key=parse_checkin) if out_records else None

				# Initialize variables
				in_time_checkin = earliest_in_record["checkin"].strftime('%H:%M:%S') if earliest_in_record else ""
				out_time_checkin = latest_out_record["checkin"].strftime('%H:%M:%S') if latest_out_record else ""
				hour_diff = ""
				status = ""
				early_out = ""
				late_in = ""

				if earliest_in_record and latest_out_record:
					# Calculate hour difference
					hour_diff = (latest_out_record["checkin"] - earliest_in_record["checkin"]).total_seconds() / 3600  # Convert seconds to hours
					hour_diff = round(hour_diff, 2)

					shift_details_doc = frappe.get_doc("Shift Type", shift)

					if hour_diff:
						# Determine attendance status
						if hour_diff > shift_details_doc.working_hours_threshold_for_half_day:
							status = "Present"
						elif hour_diff < shift_details_doc.working_hours_threshold_for_half_day and hour_diff >= shift_details_doc.working_hours_threshold_for_absent:
							status = "Half Day"
						elif hour_diff < shift_details_doc.working_hours_threshold_for_absent:
							status = "Absent"

					start_time = shift_details_doc.start_time
					end_time = shift_details_doc.end_time

					if start_time:
						# Calculate late in time
						late_entry_grace_period = shift_details_doc.late_entry_grace_period
						start_date_time = f"{frappe.utils.getdate()} {start_time}"
						late_in_time = frappe.utils.get_time(frappe.utils.add_to_date(start_date_time, minutes=late_entry_grace_period))
						in_datetime = earliest_in_record["checkin"]

						if in_datetime:
							in_time = frappe.utils.get_time(in_datetime)
							
							if in_time and in_time > late_in_time:
								in_time_diff = frappe.utils.time_diff_in_seconds(str(in_time), str(start_time))
								in_time_diff_mins = in_time_diff / 60
								late_in = round(in_time_diff_mins, 0)
					else:
						frappe.msgprint("Start time is not defined.")
					
					if end_time:
						# Calculate early out time
						early_exit_grace_period = shift_details_doc.early_exit_grace_period
						end_date_time = f"{frappe.utils.getdate()} {end_time}"
						early_out_time = frappe.utils.get_time(frappe.utils.add_to_date(end_date_time, minutes=-(early_exit_grace_period)))
						out_datetime = latest_out_record["checkin"]

						if out_datetime:
							out_time = frappe.utils.get_time(out_datetime)

							if out_time and out_time < early_out_time:
								out_time_diff = frappe.utils.time_diff_in_seconds(str(end_time), str(out_time))
								out_time_diff_mins = out_time_diff / 60
								early_out = round(out_time_diff_mins, 0)
					else:
						frappe.msgprint("End time is not defined.")

				# Append to aggregated_checkins_list regardless of whether records exist
				aggregated_checkins_list.append({
					"employee": employee,
					"date": from_date,
					"in": in_time_checkin,
					"out": out_time_checkin,
					"shift": shift,
					"hour": hour_diff,
					"status": status,
					"early_out": early_out,
					"late_in": late_in,
					"employee_checkins": f'{earliest_in_record["id"] if earliest_in_record else ""}, {latest_out_record["id"] if latest_out_record else ""}',
					"employee_checkin":earliest_in_record["id"] if earliest_in_record else "",
					"employee_checkout":latest_out_record["id"] if latest_out_record else ""
					# "attendance_requested" : "",
					# "attendance_marked" : ""
				})

		# Fetch employee list, attendance, attendance requests, and leave applications
		employee_list = frappe.db.get_list('Employee',
			filters={
				'default_shift': shift,
				'status': "Active",
				'date_of_joining':["<=", from_date]
			}, pluck="name")

		employee_att_list = frappe.db.get_list('Attendance',
			filters={
				'attendance_date': from_date,
				'docstatus': "1",
				'shift': shift
			}, fields = ["name", "employee"], as_list = False)

		employee_att_req_list = frappe.db.get_list('Attendance Request',
			filters={
				'from_date': ['<=', from_date],
				'to_date': ['>=', from_date],
				'shift': shift
			}, pluck="employee")

		leave_applications = frappe.db.get_list('Leave Application',
			filters={
				'from_date': ['<=', from_date],
				'to_date': ['>=', from_date],
				'custom_shift': shift
			},
			fields=["name", "employee", "docstatus", "from_date", "to_date", "total_leave_days", "status", "custom_shift"], as_list=False
		)

		# Ensure all employees are included in the aggregated_checkins_list
		if employee_list:
			for emp in employee_list:
				# Check if the employee is in any of the aggregated check-ins
				if not any(emp == agg.get("employee") for agg in aggregated_checkins_list):
					# If not, append a new dictionary with the employee to the aggregated_checkins_list
					aggregated_checkins_list.append({
						"employee": emp,
						"shift": shift,
						"date": from_date,
						"in": "",
						"out": "",
						"hour": "",
						"status": "",
						"early_out": "",
						"late_in": "",
						"employee_checkins": "",
						# "attendance_requested" : "",
						# "attendance_marked" : ""
					})

			leave_list = []
			if leave_applications:
				for leave_app in leave_applications:
					leave_from_date = frappe.utils.getdate(leave_app["from_date"])
					leave_to_date = frappe.utils.getdate(leave_app["to_date"])
					if leave_app["status"] == "Approved" and leave_app["docstatus"] == 1:
						approved = ""
						status = "On Leave"
					elif leave_app["status"] == "Rejected" and leave_app["docstatus"] == 1:
						approved = "No"
						status = "Rejected"
					else:
						approved = "No"
						status = "Leave Applied"
					leave_application = leave_app["name"]
					employee = leave_app["employee"]
					leave_list.append({"employee": leave_app["employee"], "date": from_date, "status": status, "leave_application": leave_app["name"], "approved": approved, "shift": leave_app["custom_shift"]})

    # Update aggregated_checkins_list with leave details if employee exists in both lists
			if leave_list:
				for leave in leave_list:
					for agg in aggregated_checkins_list:
						if agg.get("employee") == leave["employee"]:
							if agg.get("in") is None and agg.get("out") is None:
								agg.update(leave)
							else:
								agg["status"] = "Check"
								agg["leave_application"] = leave["leave_application"]
							if (agg.get("in") is None and agg.get("out")) or (agg.get("in") and agg.get("out") is None):
								agg["status"] = "Check"
								agg["approved"] = ""
								agg["leave_application"] = leave["leave_application"]
							break
					else:
						aggregated_checkins_list.append(leave)
			if employee_att_list:
				for emp in employee_att_list:
					for agg in aggregated_checkins_list:
						if agg.get("employee") == emp.get("employee"):
							# agg["attendance_marked"] = 1
							agg["attendance"] = emp.get("name")
							agg["approved"] = "Marked"
							break  # Ensure only one instance of the employee is updated
			if employee_att_req_list:
				for emp in employee_att_req_list:
					for agg in aggregated_checkins_list:
						if agg.get("employee") == emp:
							agg["attendance_requested"] = 1
							break  # Ensure only one instance of the employee is updated
			if aggregated_checkins_list:
				frappe.response["message"] = aggregated_checkins_list

	else:
		# Initialize an empty dictionary to store aggregated check-ins
		aggregated_checkins = {}
		
		# Execute SQL query to retrieve employee check-ins on specified date
		query = frappe.db.sql("""
			SELECT
				ec.name as id,
				ec.employee as employee,
				ec.custom_date as date,
				ec.log_type as log_type,
				ec.shift as shift_type,
				MIN(ec.time) as checkin
			FROM 
				`tabEmployee Checkin` AS ec
			WHERE 
				ec.docstatus = "0" AND
				ec.custom_date = %s AND 
				ec.shift = %s
			GROUP BY
				ec.employee, ec.custom_date, ec.log_type
			""", (from_date, shift), as_dict=True)
		# Loop through the query results
		employee_checkin_ids = {}
		for row in query:
			# Generate a unique key for each employee and date combination
			key = (row.employee, row.date, row.shift_type)
			# if row.shift_type:
			#     key = (row.employee, row.date, row.shift_type)
			# else:
			#     key = (row.employee, row.date, None)

			# If the key doesn't exist in the aggregated_checkins dictionary, initialize it
			if key not in aggregated_checkins:
				aggregated_checkins[key] = {
					"employee": row.employee,
					"date": row.date,
					"shift": row.shift_type,
					"work_from":row.work_from,
					"in": None,
					"out": None,
					"hour": None,
					"status":None,
					"late_in":None,
					"early_out":None,
					"employee_checkins": ""
				}
			# Convert the check-in and check-out times to datetime objects
			checkin_time = frappe.utils.get_datetime(row.checkin)
			emp_checkin = {}
			if row.log_type == "IN":
				aggregated_checkins[key]["in"] = checkin_time
				emp_checkin[aggregated_checkins[key]["employee"]] = row.id  # Correct dictionary assignment
			elif row.log_type == "OUT":
				aggregated_checkins[key]["out"] = checkin_time
				emp_checkin[aggregated_checkins[key]["employee"]] = row.id  # Correct dictionary assignment
			# Collect check-in IDs for each employee
			if row.employee not in employee_checkin_ids:
				# This creates an empty list for the employee to store their check-in IDs.
				employee_checkin_ids[row.employee] = []
			# This appends the current check-in ID (row.id) to the list of IDs for the employee.
			employee_checkin_ids[row.employee].append(row.id)
		# Assign the collected check-in IDs to the employee_checkins field in aggregated_checkins
		for key in aggregated_checkins:
			employee = aggregated_checkins[key]["employee"]
			if employee in employee_checkin_ids:
				# the <employee_checkins> field in hidden in doctype
				aggregated_checkins[key]["employee_checkins"] = ", ".join(employee_checkin_ids[employee])
				if employee_checkin_ids[employee]:
					for check in employee_checkin_ids[employee]:
						log_type = frappe.db.get_value("Employee Checkin", check, "log_type")
						if log_type == "IN":
							aggregated_checkins[key]["employee_checkin"] = check
						elif log_type == "OUT":
							aggregated_checkins[key]["employee_checkout"] = check
		# Calculate the difference in hours between check-out and check-in times
		for key, value in aggregated_checkins.items():
			checkin_time = value["in"]
			checkout_time = value["out"]
			if checkin_time and checkout_time:
				hour_difference = (checkout_time - checkin_time).total_seconds() / 3600  # Convert seconds to hours
				hour_difference = round(hour_difference, 2)
				aggregated_checkins[key]["hour"] = hour_difference
			# Cut the time from in out out and added to aggregated_checkins
			if checkin_time:
				tm = json.dumps(checkin_time, default=str)
				time_str = tm.split(" ")[1].strip('"')
				aggregated_checkins[key]["in"] = time_str[:8]
			if checkout_time:
				tm = json.dumps(checkout_time, default=str)
				time_str = tm.split(" ")[1].strip('"')
				aggregated_checkins[key]["out"] = time_str[:8]

		# Convert the aggregated_checkins dictionary to a list
		# employee_list = []
		employee_list = frappe.db.get_list('Employee',
		filters={
			'default_shift':shift,
			'status': "Active",
			'date_of_joining':["<=", from_date]
		}, pluck = "name")

		employee_att_list = frappe.db.get_list('Attendance',
		filters={
			'attendance_date':from_date,
			'docstatus': "1",
			'shift':shift
		}, fields = ["name", "employee"], as_list = False)

		employee_att_req_list = frappe.db.get_list('Attendance Request',
		filters={
			'from_date': ['<=', from_date],
			'to_date': ['>=', from_date],
			'shift' : shift
		}, pluck = "employee")
		aggregated_checkins_list = list(aggregated_checkins.values())
		for agg in aggregated_checkins_list:
			if agg.get("shift"):
				shift_details_doc = frappe.get_doc("Shift Type", agg.get("shift"))
				if agg.get("hour"):
					# Convert each value to a formatted time string
					if agg.get("hour") > shift_details_doc.working_hours_threshold_for_half_day:
						agg["status"] = "Present"
					elif agg.get("hour") < shift_details_doc.working_hours_threshold_for_half_day and agg.get("hour") >= shift_details_doc.working_hours_threshold_for_absent:
						agg["status"] = "Half Day"
					elif agg.get("hour") < shift_details_doc.working_hours_threshold_for_absent:
						agg["status"] = "Absent"
					else:
						agg["status"] = ""  # Set status to empty string if none of the conditions are met
				start_time = shift_details_doc.start_time
				end_time = shift_details_doc.end_time
				if start_time:
					late_entry_grace_period = shift_details_doc.late_entry_grace_period
					start_date_time = f"{frappe.utils.getdate()} {start_time}"
					late_in_time = frappe.utils.get_time(frappe.utils.add_to_date(start_date_time, minutes=late_entry_grace_period))
					in_time_str = agg.get("in")

					# Check if in_time_str is not None
					if in_time_str is not None:
						# Convert in_time_str to a datetime.time object
						in_time = frappe.utils.get_time(in_time_str)
						
						# Check if in_time is not None
						if in_time:
							# Check if in_time is later than late_in_time
							if in_time > late_in_time:
								in_time_diff = frappe.utils.time_diff_in_seconds(str(in_time), str(start_time))
								# late_in_dict = {"late_in":in_time_diff}
								in_time_diff_mins = in_time_diff/60
								agg["late_in"] = round(in_time_diff_mins, 0)
				else:
					# Handle the case when start_time is None
					frappe.msgprint("Start time is not defined.")
				if end_time:
					early_exit_grace_period = shift_details_doc.early_exit_grace_period
					end_date_time = f"{frappe.utils.getdate()} {end_time}"
					early_out_time = frappe.utils.get_time(frappe.utils.add_to_date(end_date_time, minutes=-(early_exit_grace_period)))
					out_time_str = agg.get("out")
					
					# Check if out_time_str is not None
					if out_time_str is not None:
						# Convert out_time_str to a datetime.time object
						out_time = frappe.utils.get_time(out_time_str)
		
						# Check if in_time is not None
						if out_time:
							# Check if in_time is later than late_in_time
							if out_time < early_out_time:
								out_time_diff = frappe.utils.time_diff_in_seconds(str(end_time), str(out_time))
								# late_in_dict = {"late_in":in_time_diff}
								out_time_diff_mins = out_time_diff/60
								agg["early_out"] = round(out_time_diff_mins, 0)
				else:
					# Handle the case when end_time is None
					frappe.msgprint("End time is not defined.")
			# Iterate over the employee_list
			for emp in employee_list:
				# Check if the employee is in any of the aggregated check-ins
				if not any(emp == agg.get("employee") for agg in aggregated_checkins_list):
					# If not, append a new dictionary with the employee to the aggregated_checkins_list
					aggregated_checkins_list.append({"employee": emp, "shift": agg.get("shift"), "date":agg.get("date")})
	
		leave_applications = frappe.db.get_list('Leave Application', 
		filters={
			'from_date': ['<=', from_date],
			'to_date': ['>=', from_date],
			'custom_shift':shift
		}, 
		fields = ["name", "employee", "docstatus", "from_date", "to_date", "total_leave_days", "status", "custom_shift"], as_list = False
		)
		leave_list = []
		if leave_applications:
			for leave_app in leave_applications:
				leave_from_date = frappe.utils.getdate(leave_app["from_date"])
				leave_to_date = frappe.utils.getdate(leave_app["to_date"])
				if leave_app["status"] == "Approved" and leave_app["docstatus"] == 1:
					approved = ""
					status = "On Leave"
				elif leave_app["status"] == "Rejected" and leave_app["docstatus"] == 1:
					approved = "No"
					status = "Rejected"
				else:
					approved = "No"
					status = "Leave Applied"
				employee = leave_app["employee"]
				leave_list.append({"employee": leave_app["employee"], "date": from_date, "status": status, "leave_application": leave_app["name"], "approved": approved, "shift": leave_app["custom_shift"]})

		# Update aggregated_checkins_list with leave details if employee exists in both lists
		if leave_list:
			for leave in leave_list:
				for agg in aggregated_checkins_list:
					if agg.get("employee") == leave["employee"]:
						if agg.get("in") is None and agg.get("out") is None:
							agg.update(leave)
						else:
							agg["status"] = "Check"
							agg["leave_application"] = leave["leave_application"]
						if (agg.get("in") is None and agg.get("out")) or (agg.get("in") and agg.get("out") is None):
							agg["status"] = "Check"
							agg["approved"] = ""
							agg["leave_application"] = leave["leave_application"]
						break
				else:
					aggregated_checkins_list.append(leave)
		if employee_att_list:
			for emp in employee_att_list:
				for agg in aggregated_checkins_list:
					if agg.get("employee") == emp.get("employee"):
						# agg["attendance_marked"] = 1
						agg["attendance"] = emp.name
						agg["approved"] = "Marked"
						break  # Ensure only one instance of the employee is updated
		if employee_att_req_list:
			for emp in employee_att_req_list:
				for agg in aggregated_checkins_list:
					if agg.get("employee") == emp:
						agg["attendance_requested"] = 1
						break  # Ensure only one instance of the employee is updated
		if aggregated_checkins_list:
			# Sort the aggregated_checkins_list by employee name in ascending order
			aggregated_checkins_list.sort(key=lambda x: x.get("employee"))
			frappe.response['message'] = aggregated_checkins_list

				# Generate all dates between from_date and to_date
				# eg if total_leave_days = 3 the range = [0, 1, 2]
				# for i in range(int(total_days)):
				#     date = frappe.utils.add_days(leave_from_date, i)
				#     all_dates.append
					# all_dates.append({"date": date, "approved" : approved, "leave_application" : leave_application})
			
			# employee_date_list = []
		
			# for emp in unique_employee_list:
			#     for date_info in all_dates:
			#         employee_date_list.append({"employee": emp, "date": date_info["date"], "status": "On Leave", "leave_application" : date_info["leave_application"],
			#         "approved":date_info["approved"], "shift" : frappe.db.get_value("Employee", emp, "default_shift")})
			# if employee_date_list:
			#     aggregated_checkins_list.extend(employee_date_list)
	
@frappe.whitelist()
def mark_daily_attendance(mark_att_tool):
	daily_mark_attendance = frappe.get_doc(mark_att_tool)

	# Initialize a counter for the number of attendance records created
	attendance_count = 0
	status_list = ["Leave Applied", "Rejected", "Check", ]
	for details in daily_mark_attendance.attendance_mark:
		if details.approved == "Yes" and details.status not in status_list and details.attendance == None:
			attendance = frappe.new_doc("Attendance")
			attendance.employee = details.employee
			attendance.status = details.status
			attendance.leave_type = details.leave_type if details.leave_type else ""
			attendance.leave_application = details.leave_application if details.leave_application else ""
			attendance.attendance_date = details.date
			attendance.late_entry = 1 if details.late_in else 0
			attendance.early_exit = 1 if details.early_out else 0
			attendance.shift = details.default_shift
			attendance.employee = details.employee
			attendance.save()
			attendance.submit()
			# Set details.attendance_marked to 1 and  details.approved = "Marked" and save the daily_mark_attendance
			# details.attendance_marked = 1
			details.approved = "Marked"
			details.attendance = attendance.name
			daily_mark_attendance.save()
			# Increment the counter after saving the attendance record
			# attendance_count = attendance_count + 1
			attendance_count += 1
			if details.employee_checkins:
				emp_checkins = details.employee_checkins.split(", ")
				for checkins in emp_checkins:
					frappe.db.set_value("Employee Checkin", checkins, "custom_attendance_marked", 1)
	# Display the count of attendance records created
	frappe.msgprint(f"<b>{attendance_count}</b> Attendance records created.")


