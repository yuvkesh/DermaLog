import requests
import json
from datetime import datetime

class WebhookSender:
    def __init__(self, webhook_url):
        self.webhook_url = webhook_url

    def send_analysis(self, analysis_data):
        payload = {
            "image_path": analysis_data["image_path"],
            "ocr_text": analysis_data["ocr_text"],
            "ai_analysis": analysis_data["ai_analysis"],
            "is_dangerous": analysis_data["is_dangerous"],
            "timestamp": datetime.utcnow().isoformat()
        }

        headers = {
            "Content-Type": "application/json"
        }

        try:
            response = requests.post(self.webhook_url, data=json.dumps(payload), headers=headers)
            response.raise_for_status()
            print(f"Webhook sent successfully. Status code: {response.status_code}")
            return True
        except requests.exceptions.RequestException as e:
            print(f"Error sending webhook: {e}")
            return False
