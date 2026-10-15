import os
import requests


class SmsService:
    def __init__(self):
        self.api_key = os.getenv("SMSIR_API_KEY")
        self.line_number = os.getenv("SMSIR_LINE_NUMBER")
        self.template_id = 672547
        self.base_url = "https://api.sms.ir/v1/send/verify"

    def send_otp(self, mobile: str, code: str) -> bool:
        headers = {
            "Content-Type": "application/json",
            "x-api-key": self.api_key
        }

        payload = {
            "mobile": mobile,
            "templateId": self.template_id,
            "parameters": [
                {"name": "CODE", "value": code}
            ]
        }

        try:
            response = requests.post(self.base_url, json=payload, headers=headers)
            data = response.json()
            print(f"DEBUG SMS Response: {data}")
            return data.get("status") == 1
        except Exception as e:
            print(f"DEBUG SMS Error: {e}")
            return False