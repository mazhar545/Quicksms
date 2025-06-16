import frappe
import os
import base64
import requests
import chardet
import openpyxl
import csv
from frappe.model.document import Document
from quicksms.sms_service import SmsService

class SendSms(Document):
	pass

@frappe.whitelist()
def process_and_send_sms(docname):
	doc = frappe.get_doc("SendSms", docname)

	if not doc.file:
		frappe.throw("Please upload a file containing phone numbers.")

	# 📁 Get file path from File Doctype
	attached_file = frappe.get_doc("File", {"file_url": doc.file})
	file_path = attached_file.get_full_path()

	# 🔢 Extract phone numbers from uploaded file
	phone_numbers = extract_phone_numbers(file_path)
	if not phone_numbers:
		frappe.throw("No valid phone numbers found in the uploaded file.")

	# 📄 Load SMS Template
	template = frappe.get_doc("Sms Templates", doc.sms_for)
	content = template.content or "Hello {code}, your appointment is on {date}"

	# 🔐 Load 4Jawaly Credentials
	settings = frappe.get_doc("QuickSMS Settings")
	app_id = settings.app_id.strip()
	app_secret = settings.get_password("app_secret").strip()
	base_url = settings.base_url.strip().rstrip("/")
	sender = getattr(settings, "sender_name", "").strip() or "Alquwwah"

	auth_string = f"{app_id}:{app_secret}"
	auth_header = "Basic " + base64.b64encode(auth_string.encode()).decode("utf-8")
	headers = {
		"Authorization": auth_header,
		"Accept": "application/json",
		"Content-Type": "application/json"
	}

	success_count = 0

	# 🔁 Send SMS to each number
	for phone in phone_numbers:
		message = content.replace("{code}", phone).replace("{date}", str(doc.date))

		payload = {
			"messages": [
				{
					"text": message,
					"numbers": [phone],
					"sender": sender
				}
			]
		}

		try:
			resp = requests.post(f"{base_url}/account/area/sms/send", headers=headers, json=payload, timeout=10)
			frappe.log_error(
    title=f"SMS Sent to {phone}",
    message=f"Status Code: {resp.status_code}\nResponse: {resp.text}"
)

			if resp.status_code == 200 and resp.json().get("code") == 200:
				success_count += 1
			else:
				frappe.log_error(str(resp.json()), f"SMS Failed for {phone}")

		except Exception as e:
			frappe.log_error(frappe.get_traceback(), f"Exception for {phone}")

	return f"{success_count} SMS sent successfully."


def extract_phone_numbers(file_path):
	ext = os.path.splitext(file_path)[1].lower()
	numbers = []

	try:
		if ext in ['.xlsx', '.xls']:
			wb = openpyxl.load_workbook(file_path)
			sheet = wb.active
			for row in sheet.iter_rows(min_row=2, values_only=True):  # Skip header
				phone = str(row[1]).strip() if row and len(row) > 1 else None
				if phone:
					numbers.append(phone)

		elif ext == '.csv':
			with open(file_path, 'rb') as f:
				raw = f.read()
				encoding = chardet.detect(raw)['encoding'] or 'utf-8'

			with open(file_path, 'r', encoding=encoding, errors='ignore') as f:
				reader = csv.reader(f)
				next(reader, None)  # Skip header
				for row in reader:
					if len(row) >= 2 and row[1].strip():
						numbers.append(row[1].strip())

	except Exception as e:
		frappe.log_error(frappe.get_traceback(), "Failed to extract phone numbers")

	return numbers




@frappe.whitelist()
def fetch_sms_balance_for_listview():
    try:
        sms_service = SmsService()
        result = sms_service.get_balance()

        if result.get("error"):
            return {"error": result["error"]}

        return {
            "success": True,
            "balance": result.get("total_balance", 0)
        }

    except Exception as e:
        return {"error": str(e)}