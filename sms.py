import africastalking
import logging
import os
import requests
from dotenv import load_dotenv
from requests.adapters import HTTPAdapter
from urllib3.util.ssl_ import create_urllib3_context

# Load environment variables
load_dotenv()

AFRICAS_TALKING_API_KEY = os.getenv("AFRICAS_TALKING_API_KEY")

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Custom adapter to force TLS 1.2
class TLSAdapter(HTTPAdapter):
    def init_poolmanager(self, *args, **kwargs):
        context = create_urllib3_context(ciphers=None, cert_reqs=None, options=None)
        kwargs['ssl_context'] = context
        return super(TLSAdapter, self).init_poolmanager(*args, **kwargs)

# Configure a custom session with the TLSAdapter
session = requests.Session()
session.mount('https://', TLSAdapter())

# Initialize Africa's Talking SDK
username = "sandbox"
africastalking.initialize(username, AFRICAS_TALKING_API_KEY)

# SMS Service
sms = africastalking.SMS

def send_sms(phone_number: str, message: str):
    try:
        response = sms.send(message, [phone_number])
        logger.info(f"SMS sent to {phone_number}. Response: {response}")
        return response
    except requests.exceptions.SSLError as ssl_err:
        logger.error(f"SSL Error when sending SMS: {ssl_err}")
        logger.info("Attempting to bypass SSL verification...")
        try:
            # Use the custom session with SSL verification disabled
            original_verify = session.verify
            session.verify = False
            response = sms.send(message, [phone_number], session=session)
            logger.info(f"SMS sent to {phone_number} with SSL verification disabled. Response: {response}")
            return response
        finally:
            # Restore original SSL verification setting
            session.verify = original_verify
    except Exception as e:
        logger.error(f"Failed to send SMS: {e}")
        raise e

# Test the SMS sending function
if __name__ == "__main__":
    test_phone_number = "+254727284935"  # Replace with a valid test phone number
    test_message = "This is a test message from your FastAPI app."
    send_sms(test_phone_number, test_message)