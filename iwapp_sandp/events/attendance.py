# import frappe

# def after_submit(doc, method):
#     emp_checkin = frappe.db.get_list("Employee Checkin", filters = {"attendance": doc.name}, pluck = "name")
#     if emp_checkin:
#         for checkin in emp_checkin:
#             frappe.db.set_value("Employee Checkin", checkin, "custom_attendance_marked", 1)