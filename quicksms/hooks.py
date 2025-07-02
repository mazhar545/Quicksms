app_name = "quicksms"
app_title = "QuickSms"
app_publisher = "Bot Solutions"
app_description = "app for sending sms"
app_email = "engrmazharali95@gmail.com"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/quicksms/css/quicksms.css"
# app_include_js = "/assets/quicksms/js/quicksms.js"

# include js, css files in header of web template
# web_include_css = "/assets/quicksms/css/quicksms.css"
# web_include_js = "/assets/quicksms/js/quicksms.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "quicksms/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
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
# 	"methods": "quicksms.utils.jinja_methods",
# 	"filters": "quicksms.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "quicksms.install.before_install"
# after_install = "quicksms.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "quicksms.uninstall.before_uninstall"
# after_uninstall = "quicksms.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "quicksms.utils.before_app_install"
# after_app_install = "quicksms.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "quicksms.utils.before_app_uninstall"
# after_app_uninstall = "quicksms.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "quicksms.notifications.get_notification_config"

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

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
# 	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"quicksms.tasks.all"
# 	],
# 	"daily": [
# 		"quicksms.tasks.daily"
# 	],
# 	"hourly": [
# 		"quicksms.tasks.hourly"
# 	],
# 	"weekly": [
# 		"quicksms.tasks.weekly"
# 	],
# 	"monthly": [
# 		"quicksms.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "quicksms.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "quicksms.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "quicksms.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["quicksms.utils.before_request"]
# after_request = ["quicksms.utils.after_request"]

# Job Events
# ----------
# before_job = ["quicksms.utils.before_job"]
# after_job = ["quicksms.utils.after_job"]

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
# 	"quicksms.auth.validate"
# ]



# Whitelisted method for API
doc_events = {}

# Make your method whitelisted
override_whitelisted_methods = {
    "quick_sms.api.routes.get_sms_balance": "quick_sms.api.routes.get_sms_balance"
}

doctype_list_js = {
    "SendSms": "public/js/sendsms_list.js"
}


fixtures = [
    {
        "dt": "Client Script",
        "filters": [
            ["name", "in", [
                "DepartmentContact",
                "SMS Settings",
                "Sms Btn",
                "Available Balance",
                "Schedule Sms"
            ]]
        ]
    },
    {
        "dt": "Custom HTML Block",
        "filters": [
            ["name", "in", [
                "Send SMS",
                "SMS  Contact List",  
                "Quick SMS Settings"
            ]]
        ]
    },
    {
        "dt": "Dashboard Chart",
        "filters": [
            ["name", "in", ["Send SMS"]]
        ]
    }
]




scheduler_events = {
    # "cron": {
    #     "* * * * *": [
    #         "quicksms.quicksms.doctype.send_sms.send_sms.process_due_scheduled_sms"
    #     ]
    # }
    "cron": {
    "*/10 * * * *": [
        "quicksms.quicksms.doctype.send_sms.send_sms.process_due_scheduled_sms"
    ]
}

}




