from datetime import datetime, timedelta
from frappe.utils import (
    add_days,
    time_diff_in_hours,
    get_time,
    getdate,
    getdate
)
from frappe import _
import frappe

@frappe.whitelist()
def update_activity_cost():
    employee_details = frappe.db.get_list("Employee", filters={"status": "Active"},
                                          fields=["name", "custom_salary_per_day", "default_shift"], as_list=0)
    if employee_details:
        for emp in employee_details:
            shift = frappe.get_doc("Shift Type", emp.get("default_shift"))
            
            # Get today's date
            today = datetime.today().date()
            
            # Combine today's date with start and end times
            start_time = datetime.combine(today, get_time(shift.start_time))
            end_time = datetime.combine(today, get_time(shift.end_time))

            # Adjust end time if the shift ends the next day
            if shift.end_time < shift.start_time:
                end_time = datetime.combine(add_days(today, 1), get_time(shift.end_time))
            
            # Calculate the time difference in hours
            hours = time_diff_in_hours(end_time, start_time)

            # Calculate costing rate
            costing_rate = emp.get("custom_salary_per_day") / hours

            # Get percent for billing rate calculation
            percent = frappe.db.get_single_value('Custom Default Values', 'percent')
            billing_rate = costing_rate * percent / 100

            # Check if activity cost exists and update or create
            activity_cost = frappe.db.exists("Activity Cost", {"employee": emp.get("name")})
            if activity_cost:
                activity = frappe.get_doc("Activity Cost", activity_cost)
                activity.costing_rate = costing_rate
                activity.billing_rate = billing_rate if percent else 0
                activity.save()
                frappe.db.commit()
            else:
                activity_new = frappe.new_doc("Activity Cost")
                activity_new.activity_type = "Execution"
                activity_new.employee = emp.get("name")
                activity_new.costing_rate = costing_rate
                activity_new.billing_rate = billing_rate if percent else 0
                activity_new.insert()
                frappe.db.commit()
    
    frappe.msgprint(_("All Activity Costs have been updated for Active Employees."))
