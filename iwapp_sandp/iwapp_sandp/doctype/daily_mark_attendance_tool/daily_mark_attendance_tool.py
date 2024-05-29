# Copyright (c) 2024, Iwex Informatics and contributors
# For license information, please see license.txt

import frappe, json
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
		
		# Create the new list of dictionaries
		result = []
		for employee, shifts in grouped_records.items():
			for shift_type, records in shifts.items():
				in_records = [rec for rec in records if rec["log_type"] == "IN"]
				out_records = [rec for rec in records if rec["log_type"] == "OUT"]
		
				if in_records:
					earliest_in_record = min(in_records, key=parse_checkin)
				else:
					earliest_in_record = None
		
				if out_records:
					latest_out_record = max(out_records, key=parse_checkin)
				else:
					latest_out_record = None
		
				if earliest_in_record and latest_out_record:
					if earliest_in_record["checkin"] and latest_out_record["checkin"]:
						# hour_diff = frappe.utils.get_time(latest_out_record["checkin"] - earliest_in_record["checkin"])
						hour_diff = (latest_out_record["checkin"] - earliest_in_record["checkin"]).total_seconds() / 3600  # Convert seconds to hours
						hour_diff = round(hour_diff, 3)
						in_time_checkin = (str(frappe.utils.get_time(earliest_in_record["checkin"]))).split(".")[0]
						out_time_checkin = (str(frappe.utils.get_time(latest_out_record["checkin"]))).split(".")[0]
						shift_details_doc = frappe.get_doc("Shift Type", shift)
						if hour_diff:
							status = ""
							# Convert each value to a formatted time string
							if hour_diff > shift_details_doc.working_hours_threshold_for_half_day:
								status = "Present"
							elif hour_diff < shift_details_doc.working_hours_threshold_for_half_day and hour_diff >= shift_details_doc.working_hours_threshold_for_absent:
								status = "Half Day"
							elif hour_diff < shift_details_doc.working_hours_threshold_for_absent:
								status = "Absent"
							else:
								status  # Set status to empty string if none of the conditions are met
						start_time = shift_details_doc.start_time
						end_time = shift_details_doc.end_time
						if start_time:
							late_in = ""
							late_entry_grace_period = shift_details_doc.late_entry_grace_period
							# for adding minutes to time
							start_date_time = f"{frappe.utils.getdate()} {start_time}"
							late_in_time = frappe.utils.get_time(frappe.utils.add_to_date(start_date_time, minutes=late_entry_grace_period))
							in_datetime = earliest_in_record["checkin"]
							
							# Check if in_time_str is not None
							if in_datetime is not None:
								# Convert in_time_str to a datetime.time object
								in_time = frappe.utils.get_time(in_datetime)
								
								# Check if in_time is not None
								if in_time:
									# Check if in_time is later than late_in_time
									if in_time > late_in_time:
										in_time_diff = frappe.utils.time_diff_in_seconds(str(in_time), str(start_time))
										# late_in_dict = {"late_in":in_time_diff}
										in_time_diff_mins = in_time_diff/60
										late_in = round(in_time_diff_mins, 0)
						else:
							# Handle the case when start_time is None
							frappe.msgprint("Start time is not defined.")
						if end_time:
							early_out = ""
							early_exit_grace_period = shift_details_doc.early_exit_grace_period
							end_date_time = f"{frappe.utils.getdate()} {end_time}"
							early_out_time = frappe.utils.get_time(frappe.utils.add_to_date(end_date_time, minutes=-(early_exit_grace_period)))
							out_datetime = latest_out_record["checkin"]
							
							# Check if out_time_str is not None
							if out_datetime is not None:
								# Convert out_time_str to a datetime.time object
								out_time = frappe.utils.get_time(out_datetime)
				
								# Check if in_time is not None
								if out_time:
									# Check if in_time is later than late_in_time
									if out_time < early_out_time:
										out_time_diff = frappe.utils.time_diff_in_seconds(str(end_time), str(out_time))
										# late_in_dict = {"late_in":in_time_diff}
										out_time_diff_mins = out_time_diff/60
										early_out = round(out_time_diff_mins, 0)
						else:
							# Handle the case when end_time is None
							frappe.msgprint("End time is not defined.")
			
					
					result.append({
						"employee": employee,
						"date": earliest_in_record["date"],
						"in": in_time_checkin,
						"out": out_time_checkin,
						"shift": earliest_in_record["shift_type"],
						"hour":hour_diff,
						"status":status,
						"early_out":early_out,
						"late_in":late_in,
						"employee_checkins": f'{earliest_in_record["id"]}, {latest_out_record["id"]}'
					})
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
				# Check if the status is "Approved"
				if leave_app["status"] == "Approved" and leave_app["docstatus"] == 1:
					approved = "Yes"
					status = "On Leave"
				else:
					approved = "No"
					status = "Leave Applied"
				leave_application = leave_app["name"]
				employee = leave_app["employee"]
				# Calculate the number of days between from_date and to_date
				total_days = leave_app["total_leave_days"]
				leave_list.append({"employee": leave_app["employee"], "date": from_date, "status": status, "leave_application" : leave_app["name"],
				"approved":approved, "shift" : leave_app["custom_shift"]})
		if leave_list:
			result.extend(leave_list)
		
		# Show the result
		frappe.response['message'] = result

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
				aggregated_checkins[key]["employee_checkins"] = ", ".join(employee_checkin_ids[employee])
				
		# Calculate the difference in hours between check-out and check-in times
		for key, value in aggregated_checkins.items():
			checkin_time = value["in"]
			checkout_time = value["out"]
			if checkin_time and checkout_time:
				hour_difference = (checkout_time - checkin_time).total_seconds() / 3600  # Convert seconds to hours
				hour_difference = round(hour_difference, 3)
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
				# Check if the status is "Approved"
				if leave_app["status"] == "Approved" and leave_app["docstatus"] == 1:
					approved = "Yes"
					status = "On Leave"
				else:
					approved = "No"
					status = "Leave Applied"
				leave_application = leave_app["name"]
				employee = leave_app["employee"]
				# Calculate the number of days between from_date and to_date
				total_days = leave_app["total_leave_days"]
				leave_list.append({"employee": leave_app["employee"], "date": from_date, "status": status, "leave_application" : leave_app["name"],
				"approved":approved, "shift" : leave_app["custom_shift"]})
		if leave_list:
			aggregated_checkins_list.extend(leave_list)
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

		if aggregated_checkins_list:
			frappe.response['message'] = aggregated_checkins_list
	
@frappe.whitelist()
def mark_daily_attendance(employee_checkins):
	daily_mark_attendance = frappe.get_doc(employee_checkins)

	# Initialize a counter for the number of attendance records created
	attendance_count = 0

	for details in daily_mark_attendance.attendance_mark:
		if details.approved == "Yes" and details.status != "Leave Applied":
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
			# Increment the counter after saving the attendance record
			attendance_count = attendance_count + 1
			if details.employee_checkins:
				emp_checkins = details.employee_checkins.split(", ")
				for checkins in emp_checkins:
					frappe.db.set_value("Employee Checkin", checkins, "custom_attendance_marked", 1)
	# Display the count of attendance records created
	frappe.msgprint(f"<b>{attendance_count}</b> Attendance records created.")


