# Copyright (c) 2025, Bot Solutions and contributors
# For license information, please see license.txt

import frappe

def execute(filters=None):
    # Define columns for the report
    columns = [
        {
            "label": "Code", 
            "fieldname": "code", 
            "fieldtype": "Data", 
            "width": 150
        },
        {
            "label": "Phone Number", 
            "fieldname": "phone_number", 
            "fieldtype": "Data", 
            "width": 150
        },
        {
            "label": "Status", 
            "fieldname": "status", 
            "fieldtype": "Data", 
            "width": 150
        },
        {
            "label": "SMS Template", 
            "fieldname": "sms_for", 
            "fieldtype": "Data", 
            "width": 150
        },
        {
            "label": "Date", 
            "fieldname": "date", 
            "fieldtype": "Date", 
            "width": 150
        },
        {
            "label": "Department", 
            "fieldname": "department", 
            "fieldtype": "Link", 
            "options": "Contact Department", 
            "width": 150
        }
    ]
    
    data = []

    # Get all the "Send SMS" documents within the provided filters (if any)
    send_sms_docs = frappe.get_all("Send SMS", filters=filters, fields=["name", "sms_for", "date", "department"])

    # Loop through each Send SMS document
    for doc in send_sms_docs:
        # Get the child table "Send Sms Number" for each Send SMS document, including the individual status for each number
        sms_numbers = frappe.get_all(
            "Send Sms Number", 
            filters={"parent": doc.name}, 
            fields=["code", "phone_number", "status"]  # Fetching the 'status' field from child doctype
        )

        # Add each phone number, its code, and the child document's status and other fields to the data list
        for number in sms_numbers:
            data.append({
                "code": number.code,
                "phone_number": number.phone_number,
                "status": number.status,  # Get individual status from the child doctype
                "sms_for": doc.sms_for,  # Add SMS template field
                "date": doc.date,  # Add date field
                "department": doc.department  # Add department field
            })
    
    return columns, data
