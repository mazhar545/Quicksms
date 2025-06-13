import frappe
import os
import base64
import requests
import chardet
from frappe.model.document import Document

class SendSms(Document):
	pass

@frappe.whitelist()
def process_and_send_sms(docname):
	doc = frappe.get_doc("SendSms", docname)

	if not doc.file:
		frappe.throw("Please upload a file containing phone numbers.")

	# Get attached file path
	attached_file = frappe.get_doc("File", {"file_url": doc.file})
	file_path = attached_file.get_full_path()

	# 🔍 Detect encoding safely
	with open(file_path, 'rb') as f:
		raw_data = f.read()
		encoding = chardet.detect(raw_data)['encoding'] or 'utf-8'

	# 📖 Read phone numbers with correct encoding
	try:
		with open(file_path, 'r', encoding=encoding, errors='ignore') as f:
			numbers = [line.strip() for line in f if line.strip()]
	except Exception as e:
		frappe.throw(f"File read error: {str(e)}")

	# Load template
	template = frappe.get_doc("Sms Templates", doc.sms_for)
	content = template.content  # should include {code} and {date}

	# Load 4Jawaly credentials
	settings = frappe.get_doc("QuickSMS Settings")
	app_id = settings.app_id.strip()
	app_secret = settings.get_password("app_secret").strip()
	base_url = settings.base_url.strip()
	sender = getattr(settings, "sender_name", "")  # optional field

	# Create auth header
	auth_string = f"{app_id}:{app_secret}"
	auth_header = "Basic " + base64.b64encode(auth_string.encode()).decode("utf-8")
	headers = {
		"Authorization": auth_header,
		"Accept": "application/json",
		"Content-Type": "application/json"
	}

	success_count = 0
	for number in numbers:
		message = content.replace("{code}", number).replace("{date}", str(doc.date))
		payload = {
			"mobile": number,
			"message": message,
			"sender": sender
		}

		try:
			resp = requests.post(f"{base_url}/sms/messages", headers=headers, json=payload, timeout=10)
			resp.raise_for_status()
			success_count += 1
		except Exception as e:
			frappe.log_error(frappe.get_traceback(), f"Failed to send SMS to {number}")

	return f"{success_count} SMS sent successfully."
