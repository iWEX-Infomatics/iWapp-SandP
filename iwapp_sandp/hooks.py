app_name = "iwapp_sandp"
app_title = "iWapp-SandP"
app_publisher = "Iwex Informatics"
app_description = "iWapp-SandP"
app_email = "emails@iwex.in"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/iwapp_sandp/css/iwapp_sandp.css"
# app_include_js = "/assets/iwapp_sandp/js/iwapp_sandp.js"

# include js, css files in header of web template
# web_include_css = "/assets/iwapp_sandp/css/iwapp_sandp.css"
# web_include_js = "/assets/iwapp_sandp/js/iwapp_sandp.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "iwapp_sandp/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
doctype_js = {"Purchase Order" : "public/js/purchase_order.js",
"Purchase Receipt" : "public/js/purchase_receipt.js",
"Purchase Invoice" : "public/js/purchase_invoice.js",
"Customer" : "public/js/customer.js", "Supplier" : "public/js/supplier.js",
"Stock Entry" : "public/js/stock_entry.js", "Stock Reconciliation" : "public/js/stock_reconciliation.js",
"Sales Order" : "public/js/sales_order.js", "Delivery Note" : "public/js/delivery_note.js",
"Sales Invoice" : "public/js/sales_invoice.js", "Pick List" : "public/js/pick_list.js",
"Material Request" : "public/js/material_request.js", "Item" : "public/js/item.js",
"Installation Note" : "public/js/installation_note.js", "Employee Checkin" : "public/js/employee_checkin.js",
"Task" : "public/js/task.js", "Opportunity" : "public/js/opportunity.js",
"Quotation" : "public/js/quotation.js", "Payment Entry" : "public/js/payment_entry.js",
"Blanket Order" : "public/js/blanket_order.js", "Issue" : "public/js/issue.js",
"Journal Entry" : "public/js/journal_entry.js", "Address" : "public/js/address.js",
"Payroll Entry" : "public/js/payroll.js", "Project" : "public/js/project.js"
}
doctype_list_js = {"Customer" : "public/js/customer_list.js",
"Supplier" : "public/js/supplier_list.js",
"Serial No" : "public/js/serial_no_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "iwapp_sandp.utils.jinja_methods",
# 	"filters": "iwapp_sandp.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "iwapp_sandp.install.before_install"
# after_install = "iwapp_sandp.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "iwapp_sandp.uninstall.before_uninstall"
# after_uninstall = "iwapp_sandp.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "iwapp_sandp.utils.before_app_install"
# after_app_install = "iwapp_sandp.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "iwapp_sandp.utils.before_app_uninstall"
# after_app_uninstall = "iwapp_sandp.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "iwapp_sandp.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
	# "*": {
	# 	"on_update": "method",.py
	# 	"on_cancel": "method",
	# 	"on_trash": "method"
	# }
    "Purchase Order": {
        "validate": "iwapp_sandp.events.purchase_order.validate",
        "before_save": "iwapp_sandp.events.purchase_order.before_save"
	},
     "Purchase Receipt": {
        "validate": "iwapp_sandp.events.purchase_receipt.validate",
        "before_save": "iwapp_sandp.events.purchase_receipt.before_save",
        "on_submit": "iwapp_sandp.events.purchase_receipt.on_submit"
	},
    "Purchase Invoice": {
        "validate": "iwapp_sandp.events.purchase_invoice.validate"
	},
     "Customer": {
        "before_save": "iwapp_sandp.events.customer.before_save"
	},
    "Supplier": {
        "before_save": "iwapp_sandp.events.supplier.before_save"
	},
    "Stock Entry": {
        "validate": "iwapp_sandp.events.stock_entry.validate",
        "before_save": "iwapp_sandp.events.stock_entry.before_save"
	},
    "Delivery Note": {
        "validate": "iwapp_sandp.events.delivery_note.validate",
        # "after_insert": "iwapp_sandp.events.delivery_note.after_insert",
        "before_save": "iwapp_sandp.events.delivery_note.before_save"
    },
    "Sales Invoice": {
        "validate": "iwapp_sandp.events.sales_invoice.validate",
        "before_save": "iwapp_sandp.events.sales_invoice.before_save"
    },
    "Sales Order": {
        "validate": "iwapp_sandp.events.sales_order.validate"
    },
    "Pick List": {
        "validate": "iwapp_sandp.events.pick_list.validate",
        "before_save": "iwapp_sandp.events.pick_list.before_save"
    },
    "Stock Reconciliation": {
        "validate": "iwapp_sandp.events.stock_reconciliation.validate",
        "on_submit": "iwapp_sandp.events.stock_reconciliation.on_submit"
    },
    "Serial No": {
        "before_save": "iwapp_sandp.events.serial_no.before_save"
    },
     "Item": {
        "before_save": "iwapp_sandp.events.item.before_save",
        # "after_insert": "iwapp_sandp.events.item.after_insert"
    },
    "Installation Note": {
        "validate": "iwapp_sandp.events.installation_note.validate",
        "before_save": "iwapp_sandp.events.installation_note.before_save"
    },
    "Quotation": {
        "validate": "iwapp_sandp.events.quotation.validate",
        # "before_save": "iwapp_sandp.events.quotation.before_save"
    },
    "Expense Claim": {
        "after_insert": "iwapp_sandp.events.expense_claim.after_insert",
    },
    "Employee": {
        "before_save" : "iwapp_sandp.events.employee.before_save",
        "after_insert" : "iwapp_sandp.events.employee.after_insert"
    },
     "Payroll Entry": {
        "before_save": "iwapp_sandp.events.payroll.before_save",
    },
    "Salary Structure Assignment": {
        "before_save": "iwapp_sandp.events.ss_assignment.before_save",
    },
    "Employee Checkin": {
        "before_save": "iwapp_sandp.events.employee_checkin.before_save",
    },
    # "Attendance":{
    #     "after_submit": "iwapp_sandp.events.attendance.after_submit",
    # }
}

# Scheduled Tasks
# ---------------

scheduler_events = {
# 	"all": [
# 		"iwapp_sandp.tasks.all"
# 	],
	"daily": [
		"iwapp_sandp.events.employee.set_age_and_service_schedular"
	],
# 	"hourly": [
# 		"iwapp_sandp.tasks.hourly"
# 	],
# 	"weekly": [
# 		"iwapp_sandp.tasks.weekly"
# 	],
# 	"monthly": [
# 		"iwapp_sandp.tasks.monthly"
# 	],
}

# Testing
# -------

# before_tests = "iwapp_sandp.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "iwapp_sandp.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "iwapp_sandp.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["iwapp_sandp.utils.before_request"]
# after_request = ["iwapp_sandp.utils.after_request"]

# Job Events
# ----------
# before_job = ["iwapp_sandp.utils.before_job"]
# after_job = ["iwapp_sandp.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"iwapp_sandp.auth.validate"
# ]

fixtures = [{
    "dt":"Custom Field",
    "filters": [
        ["name", "in", (
            "Item-custom_has_model_id", "Item-custom_model_id",
            "Purchase Order Item-custom_has_model_id", "Purchase Order Item-custom_model_id",
            "Purchase Receipt Item-custom_has_model_id", "Purchase Receipt Item-custom_model_id",
            "Purchase Receipt-custom_quick_item_entry", "Purchase Receipt-custom_purchase_item_entry",
            "Purchase Invoice Item-custom_has_model_id", "Purchase Invoice Item-custom_model_id",
            "Purchase Order Item-custom_has_serial_no", "Purchase Receipt Item-custom_has_serial_no",
            "Serial No-custom_model_id", "Stock Entry Detail-custom_model_id", "Stock Reconciliation Item-custom_model_id",
            "Purchase Invoice Item-custom_has_serial_no", "Delivery Note Item-custom_model_id",
            "Sales Invoice Item-custom_model_id", "Pick List Item-custom_model_id", "Item-custom_item_tax_percentage",
            "Material Request Item-custom_model_id", "Item-custom_item_default", "Serial No-custom_update_model_id",
            "Installation Note Item-custom_model_id", "Stock Reconciliation Item-custom_brand",
            "Stock Entry Detail-custom_brand", "Pick List Item-custom_brand", "Installation Note Item-custom_brand",
            "Stock Reconciliation Item-custom_section_break_m0cwa", "Stock Reconciliation Item-custom_description",
            "Sales Order Item-custom_model_id", "Purchase Receipt Item-custom_from_model_id", "Purchase Order Item-custom_from_model_id",
            "Sales Invoice Item-custom_from_model_id", "Sales Order Item-custom_from_model_id", "Delivery Note Item-custom_from_model_id",
            "Pick List Item-custom_from_model_id", "Stock Entry Detail-custom_from_model_id", "Stock Reconciliation Item-custom_from_model_id",
            "Installation Note Item-custom_from_model_id", "Employee Checkin-custom_date", "Opportunity-custom_project_site_details",
            "Opportunity-custom_site_address", "Opportunity-custom_site_address_html", "Task-custom_project_name",
            "Task-custom_customer", "Task-custom_project_site_details", "Task-custom_site_address", "Task-custom_site_address_html",
            "Quotation-custom_project_site_details", "Quotation-custom_site_address", "Quotation-custom_site_address_html",
            "Sales Order-custom_project_site_details", "Sales Order-custom_site_address", "Sales Order-custom_site_address_html",
            "Sales Order-custom_project_name", "Material Request Item-custom_project_name", "Material Request-custom_project_site_details",
            "Material Request-custom_site_address_html", "Material Request-custom_site_address", "Stock Entry Detail-custom_project_name",
            "Stock Entry-custom_project_site_details", "Stock Entry-custom_site_address", "Stock Entry-custom_site_address_html",
            "Stock Entry-custom_project_name", "Stock Entry-custom_customer", "Stock Entry-custom_column_break_htdrj",
            "Purchase Order-custom_project_name", "Purchase Order-custom_project_site_details", "Purchase Order-custom_site_address",
            "Purchase Order-custom_site_address_html", "Purchase Receipt Item-custom_project_name", "Purchase Receipt-custom_customer",
            "Purchase Receipt-custom_project_name", "Purchase Receipt-custom_project_site_details", "Purchase Receipt-custom_site_address",
            "Purchase Receipt-custom_site_address_html", "Purchase Invoice Item-custom_project_name", "Purchase Invoice-custom_customer",
            "Purchase Invoice-custom_project_name", "Purchase Invoice-custom_project_site_details", "Purchase Invoice-custom_site_address",
            "Purchase Invoice-custom_site_address_html", "Delivery Note Item-custom_project_name", "Delivery Note-custom_project_name",
            "Delivery Note-custom_site_address", "Delivery Note-custom_site_address_html", "Delivery Note-custom_project_site_details",
            "Installation Note-custom_project_site_details", "Installation Note-custom_site_address", "Installation Note-custom_site_address_html",
            "Sales Invoice Item-custom_project_name", "Sales Invoice-custom_project_name", "Sales Invoice-custom_project_site_details",
            "Sales Invoice-custom_site_address", "Sales Invoice-custom_site_address_html", "Payment Entry-custom_project_name",
            "Payment Entry-custom_project_site_details", "Payment Entry-custom_site_address", "Payment Entry-custom_site_address_html",
            "Blanket Order-custom_project_site_details", "Blanket Order-custom_site_address", "Blanket Order-custom_site_address_html",
            "Issue-custom_project_name", "Issue-custom_project_site_details", "Issue-custom_site_address", "Issue-custom_site_address_html",
            "Journal Entry Account-custom_customer", "Journal Entry Account-custom_project_name", "Journal Entry Account-custom_project_site_details",
            "Journal Entry Account-custom_site_address", "Journal Entry Account-custom_site_address_html", "Journal Entry Account-custom_display_site_address",
            "Journal Entry Account-custom_column_break_497ed", "Sales Invoice Item-custom_has_model_id", "Quotation Item-custom_model_id",
            "Quotation Item-custom_has_model_id", "Quotation Item-custom_from_model_id", "Purchase Order-custom_customer", "Address-custom_location",
            "Customer-custom_default_values", "Supplier-custom_default_values", "Delivery Note Item-custom_has_batch_no",
            "Sales Order Item-custom_has_batch_no", "Batch-custom_brand", "Batch-custom_model_id", "Purchase Receipt Item-custom_has_batch_no",
            "Delivery Note Item-custom_has_model_id", "Delivery Note Item-custom_has_serial_no", "Sales Order Item-custom_has_serial_no",
            "Sales Order Item-custom_has_model_id", "Delivery Note Item-custom_model_wise_serial", "Purchase Receipt Item-custom_item_group",
            "Employee Checkin-custom_location", "Employee Checkin-custom_selfie", "Employee Checkin-custom_attendance_marked",
            "Employee Checkin-custom_work_from", "Leave Application-custom_shift", "Leave Application-custom_abbr",
            'Employee-custom_work_from', 'Employee-custom_column_break_g2lqt', 'Employee-custom_age',
            'Employee-custom_service', 'Employee-custom_column_break_7jvv2', 'Employee-custom_office_location',
            'Employee-custom_home_location', 'Employee-custom_session_expiry_mobile', 'Employee-custom_section_break_ipltb',
            'Employee-custom_leave_policy', 'Employee-custom_payable_account', 'Employee-custom_aadhaar_id',
            'Employee-custom_net_pay', 'Employee-custom_gross_salary', 'Employee-custom_basic_pay', 'Employee-custom_da',
            'Employee-custom_hra', 'Employee-custom_column_break_aifvf', 'Employee-custom_performance_allowance', 'Employee-custom_seniority_allowance',
            'Employee-custom_accommodation_allowance', 'Employee-custom_professional_tax', 'Employee-custom_salary_per_day', 'Employee-custom_esi_applicable',
            'Employee-custom_epf_applicable', 'Employee-custom_column_break_p3ofw', 'Employee-custom_uan', 'Employee-custom_esi_id', 'Employee-custom_epf_id',
            'Employee-custom_column_break_ai5hr', 'Employee-custom_section_break_ltmhr', 'Material Request-custom_task', 'Project-custom_project_site_details',
            'Project-custom_site_address', 'Project-custom_site_address_html', "Employee-custom_work_site", "Employee-custom_barcode"
            )]
    ]
    },
    {"dt":"Property Setter",
        "filters": [
            ["doc_type", "in", (
                "Supplier",
                "Customer",
                "Delivery Note Item",
                "Purchase Receipt Item",
                "Purchase Invoice Item",
                "Purchase Order Item",
                "Sales Invoice Item",
                "Sales Order Item",
                "Project",
                "Item",
                "Employee Checkin",
                "Leave Application",
                "Employee",
                "Salary Structure Assignment",
                "Expense Claim Detail"
            )]
        ]
    }
    # {
    #     "dt": "Translation",
    #     "filters": [
    #             ["name", "in", ("ec0adfc6e5")]
    #     ],
    # }
]
