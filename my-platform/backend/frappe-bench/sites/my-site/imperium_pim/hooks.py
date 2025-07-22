app_name = "imperium_pim"
app_title = "Imperium PIM"
app_publisher = "Imperium Systems & Consulting"
app_description = "PIM for Imperium Systems internal use"
app_email = "wpatrickmorgan@gmail.com"
app_license = "mit"

# Apps
# ------------------

# required_apps = []

# Each item in the list will be shown as an app in the apps page
add_to_apps_screen = [
	{
		"name": "imperium_pim",
		"logo": "/assets/imperium_pim/logo.png",
		"title": "Imperium PIM",
		"route": "/pim",
		"has_permission": "imperium_pim.api.permission.has_app_permission"
	}
]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/imperium_pim/css/imperium_pim.css"
# app_include_js = "/assets/imperium_pim/js/imperium_pim.js"

# Desktop configuration
app_include_desktop = "imperium_pim/config/desktop.py"

# Workspace configuration
app_include_workspace = "imperium_pim/config/workspace.py"

# include js, css files in header of web template
# web_include_css = "/assets/imperium_pim/css/imperium_pim.css"
# web_include_js = "/assets/imperium_pim/js/imperium_pim.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "imperium_pim/public/scss/website"

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

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "imperium_pim/public/icons.svg"

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
# 	"methods": "imperium_pim.utils.jinja_methods",
# 	"filters": "imperium_pim.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "imperium_pim.install.before_install"
# after_install = "imperium_pim.install.after_install"

# Fixtures
# --------
# Export fixtures for this app
fixtures = ["Page"]

# Uninstallation
# ------------

# before_uninstall = "imperium_pim.uninstall.before_uninstall"
# after_uninstall = "imperium_pim.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "imperium_pim.utils.before_app_install"
# after_app_install = "imperium_pim.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "imperium_pim.utils.before_app_uninstall"
# after_app_uninstall = "imperium_pim.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "imperium_pim.notifications.get_notification_config"

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
# 		"imperium_pim.tasks.all"
# 	],
# 	"daily": [
# 		"imperium_pim.tasks.daily"
# 	],
# 	"hourly": [
# 		"imperium_pim.tasks.hourly"
# 	],
# 	"weekly": [
# 		"imperium_pim.tasks.weekly"
# 	],
# 	"monthly": [
# 		"imperium_pim.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "imperium_pim.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "imperium_pim.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "imperium_pim.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["imperium_pim.utils.before_request"]
# after_request = ["imperium_pim.utils.after_request"]

# CORS Configuration for Frontend/Backend Separation
# --------------------------------------------------
before_request = ["imperium_pim.utils.handle_cors"]

# Job Events
# ----------
# before_job = ["imperium_pim.utils.before_job"]
# after_job = ["imperium_pim.utils.after_job"]

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
# 	"imperium_pim.auth.validate"
# ]

# Desktop
# --------
# Desktop configuration for module visibility in Desk UI
desktop_icons = [
    "Pim"
]

# Workspaces
# ----------
# List of workspaces to be created for this app
workspaces = [
    {
        "name": "Pim",
        "category": "Modules"
    }
]

# Installation hooks
# ------------------
# Hook to run after app installation
after_install = "imperium_pim.utils.setup_module"

# Hook to run after migration
after_migrate = "imperium_pim.utils.sync_desktop_icons"

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }

# Custom bench commands
# ---------------------
# Register custom bench commands for this app
# Note: Commands temporarily disabled due to pickling issues
# from imperium_pim.commands import commands
