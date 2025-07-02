// Copyright (c) 2025, Bot Solutions and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["SMS Status Report"] = {
	"filters": [
		{
			"fieldname": "sms_for",
			"label": __("SMS Template"),
			"fieldtype": "Link",
			"options": "SMS Templates",
			"width": 150
		},
		{
			"fieldname": "date",
			"label": __("Date"),
			"fieldtype": "Date",
			"width": 150
		}
	]
};
