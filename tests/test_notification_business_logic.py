import json
import unittest
from BusinessLogic.notification_business_logic import NotificationBusinessLogic


class FakeSmsService:
    def __init__(self):
        self.sent = []

    def send_otp(self, mobile, code):
        self.sent.append((mobile, code))
        return True


class TestNotificationBusinessLogic(unittest.TestCase):
    def setUp(self):
        self.sms_service = FakeSmsService()
        self.business_logic = NotificationBusinessLogic(self.sms_service)

    def test_process_sends_the_code_to_the_phone(self):
        body = json.dumps({"phone": "09120000002", "content": "12345"}).encode()

        self.business_logic.process(body)

        self.assertEqual(self.sms_service.sent, [("09120000002", "12345")])

    def test_process_sends_one_sms_for_each_message(self):
        self.business_logic.process(json.dumps({"phone": "09120000002", "content": "11111"}).encode())
        self.business_logic.process(json.dumps({"phone": "09120000003", "content": "22222"}).encode())

        self.assertEqual(len(self.sms_service.sent), 2)

    def test_process_rejects_a_message_that_is_not_json(self):
        with self.assertRaises(ValueError):
            self.business_logic.process(b"not json")

    def test_process_rejects_a_message_without_phone(self):
        body = json.dumps({"content": "12345"}).encode()

        with self.assertRaises(KeyError):
            self.business_logic.process(body)
        self.assertEqual(self.sms_service.sent, [])
