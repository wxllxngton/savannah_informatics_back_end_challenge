import os
import africastalking
from dotenv import load_dotenv

class AfricastalkingModel:
    """
    A class to handle interactions with Africa's Talking API.
    This class is responsible for sending SMS using Africa's Talking service.

    Methods:
        send_sms(message: str, recepients: list) -> dict:
            Sends an SMS to a list of recepient numbers.
    """

    def __init__(self):
        """
        Initializes the AfricastalkingModel by loading environment variables for API credentials.
        Initializes Africa's Talking service with the SMS service ready to use.
        """
        # Load environment variables from .env file
        load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))

        # Retrieve Africa's Talking API credentials from the environment variables
        username = os.getenv("AT_USERNAME")
        key = os.getenv("AT_KEY")

        if not username or not key:
            raise ValueError("Africa's Talking credentials (username or key) missing in environment variables.")

        # Initialize Africa's Talking API
        africastalking.initialize(username=username, api_key=key)

        # Initialize the SMS service
        self.sms = africastalking.SMS

        # Fetch AT sender shortcode
        self.short_code = os.getenv("AT_SHORTCODE")

    def send_sms(self, message: str, recepients: list) -> dict:
        """
        Sends an SMS to the specified recepients using Africa's Talking API.

        Args:
            message (str): The SMS message content to be sent.
            recepients (list): A list of recipient phone numbers in international format.

        Returns:
            dict: The response from Africa's Talking API, or an error message in case of failure.
        """
        if not message:
            return {"error": "Message content is empty."}

        if not recepients or not isinstance(recepients, list):
            return {"error": "recepients must be a non-empty list."}

        try:
            sender = self.short_code
            # Send the SMS and return the API response
            response = self.sms.send(message, recepients, sender)
            return response
        except Exception as e:
            # Handle and return the error
            return {"error": str(e)}
