from frappe.utils import getdate, date_diff, today, time_diff_in_hours, get_time, add_days
from datetime import datetime, timedelta
from frappe import _
import frappe

def calculate_years_since(date):
    """Calculate the number of years since the given date."""
    days_since = date_diff(today(), getdate(date))

    # Adjust if the date has not occurred yet this year
    if getdate(today()).month < getdate(date).month or (
        getdate(today()).month == getdate(date).month
        and getdate(today()).day < getdate(date).day
    ):
        days_since -= 1

    # Calculate the age in years
    days_since_in_years = days_since / 365.25  # Use 365.25 to account for leap years
    return days_since_in_years

def before_save(doc, method):
    monthly_salary = doc.custom_gross_salary or 0
    # Calculate the ctc
    doc.ctc = monthly_salary * 12
    # Calculate the salary per day
    doc.custom_salary_per_day = monthly_salary / 30
    doj = doc.date_of_joining
    dob = doc.date_of_birth
    if dob:
        age_in_years = calculate_years_since(dob)
        doc.custom_age = age_in_years  # Set the calculated age to custom_age field
    if doj:
        service_in_years = calculate_years_since(doj)
        doc.custom_service = service_in_years  # Set the calculated service to custom_service

def after_insert(doc, method):
    frappe.db.set_value("Employee", doc.name, "custom_barcode", doc.name)
    if doc.status == "Active" and doc.custom_salary_per_day and doc.default_shift:
        shift = frappe.get_doc("Shift Type", doc.default_shift)
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
        costing_rate = doc.custom_salary_per_day/hours
        percent = frappe.db.get_single_value('Custom Default Values', 'percent')
        billing_rate = costing_rate * percent/100

    # Create a new "Activity Cost" document
        activity_cost_doc = frappe.get_doc({
        "doctype": "Activity Cost",
        "activity_type": "Execution",
        "employee": doc.name,
        "costing_rate": costing_rate,
        "billing_rate" : billing_rate if percent else 0
        })
        # Save the document
        activity_cost_doc.insert()
        frappe.db.commit()
        frappe.msgprint(_(f"<b>Activity Cost</b> created for Employee <b>{doc.employee_name}</b>"))
    
@frappe.whitelist()
def set_age_and_service_schedular():
    employee_list = frappe.db.get_list("Employee", filters = {"status":"Active"},
                        fields = ["name","date_of_joining", "date_of_birth"], as_list = False)
    if employee_list:
        for emp in employee_list:
            dob = getdate(emp.get("date_of_birth"))
            doj = getdate(emp.get("date_of_joining"))
            if dob:
                age_in_years = calculate_years_since(dob)
                frappe.db.set_value("Employee", emp.get("name"), "custom_age", age_in_years)
            if doj:
                service_in_years = calculate_years_since(doj)
                frappe.db.set_value("Employee", emp.get("name"), "custom_service", service_in_years)
