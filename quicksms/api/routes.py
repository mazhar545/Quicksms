import frappe
from quicksms.sms_service import SmsService

@frappe.whitelist()
def test_connection():
    try:
        sms_service = SmsService()
        result = sms_service.get_balance()

        if result.get("error"):
            update_connection_status("Failed", 0)
            return {"success": False, "error": result["error"]}

        # Extract and update available balance
        balance = result.get("total_balance", 0)
        update_connection_status("Success", balance)

        return {
            "success": True,
            "message": "Connection successful",
            "available_balance": balance
        }
    except Exception as e:
        update_connection_status("Failed", 0)
        return {"success": False, "error": str(e)}

def update_connection_status(status, balance):
    settings = frappe.get_doc("Quick SMS Settings")
    settings.last_connection_status = status
    settings.available_balance = balance
    settings.save(ignore_permissions=True)
    frappe.db.commit()

@frappe.whitelist()
def get_sms_balance():
    try:
        sms_service = SmsService()
        return sms_service.get_balance()
    except Exception as e:
        return {"error": str(e)}


