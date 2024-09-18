import unittest
from models.africastalking_model import AfricastalkingModel

class TestAfricastalkingModel(unittest.TestCase):
    def setUp(self):
        """
        Set up AfricastalkingModel instance before each test case.
        This method is called before every test function to initialize the AfricastalkingModel.
        """
        self.africastalking_model = AfricastalkingModel()

    def test_at_send_sms(self):
        """
        Test Africastalking send_sms method with a valid message and recipient.
        """
        response = self.africastalking_model.send_sms("Example Message", ['+254777777777'])
        self.assertIn('SMSMessageData', response)

    def test_at_send_sms_empty_message(self):
        """
        Test Africastalking send_sms method with an empty message.
        """
        response = self.africastalking_model.send_sms(message="", recipients=['+254777777777'])
        self.assertEqual(response['error'], "Message content is empty.")

    def test_at_send_sms_empty_recipients(self):
        """
        Test Africastalking send_sms method with an empty recipient list.
        """
        response = self.africastalking_model.send_sms(message="Example message", recipients=[])
        self.assertEqual(response['error'], "recipients must be a non-empty list.")


if __name__ == "__main__":
    unittest.main()
