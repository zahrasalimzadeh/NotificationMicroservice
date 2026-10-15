import json
from Common.Services.sms_service import SmsService


class NotificationBusinessLogic:
    def __init__(self):
        self.sms_service = SmsService()

    def process(self, body):
        dictionary = json.loads(body)
        print(dictionary)
        self.sms_service.send_otp(dictionary["phone"], dictionary["content"])