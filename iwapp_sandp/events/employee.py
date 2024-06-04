from frappe.utils import getdate, date_diff, today
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
