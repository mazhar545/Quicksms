import frappe
import requests

@frappe.whitelist()
def send_sms(receiver, message):
    settings = frappe.get_single("QuickSMS Settings")

    payload = {
        "apiKey": settings.api_key,
        "sender": settings.sender_name,
        "numbers": receiver,
        "message": message 
        
    }

    try:
        response = requests.post(settings.api_url, json=payload, timeout=10)
        response.raise_for_status()
        result = response.json()
        return {
            "status": "success" if result.get("status") == "success" else "error",
            "response": result
        }
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Jawaly SMS Error")
        return {"status": "error", "error": str(e)}
