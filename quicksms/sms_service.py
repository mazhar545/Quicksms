import base64
import requests
import frappe

class SmsService:
    def __init__(self):
        settings = frappe.get_doc("QuickSMS Settings")

        self.app_id = settings.app_id.strip()
        self.app_secret = settings.get_password("app_secret").strip()  # ✅ For older Frappe versions
        self.base_url = settings.base_url.strip()

        if not self.app_id or not self.app_secret or not self.base_url:
            raise Exception("Missing SMS credentials in QuickSMS Settings")

        # Create Basic Auth header
        auth_string = f"{self.app_id}:{self.app_secret}"
        self.auth_header = "Basic " + base64.b64encode(auth_string.encode()).decode("utf-8")

        self.headers = {
            "Authorization": self.auth_header,
            "Accept": "application/json",
            "Content-Type": "application/json"
        }

    def get_balance(self):
        url = f"{self.base_url}/account/area/me/packages"
        params = {
            "is_active": 1,
            "order_by": "id",
            "order_by_type": "desc",
            "page": 1,
            "page_size": 10,
            "return_collection": 1
        }

        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            frappe.log_error(frappe.get_traceback(), "4Jawaly SMS: Balance Fetch Error")
            return {"error": str(e)}
