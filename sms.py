import africastalking
import logging
import os
import secrets
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

AFRICAS_TALKING_API_KEY = os.getenv("AFRICAS_TALKING_API_KEY")


# Initialize Africa's Talking SDK
username = "sandbox"
AFRICAS_TALKING_API_KEY = "atsk_8e66e566ccea1388dc3539da92d319961e62225ef1121e1de608247c4f5d1123bf0422d3"
africastalking.initialize(username, AFRICAS_TALKING_API_KEY)

# SMS Service
sms = africastalking.SMS

# Set up logging
logger = logging.getLogger(__name__)

def send_sms(phone_number: str, message: str):
    try:
        response = sms.send(message, [phone_number])
        logger.info(f"SMS sent to {phone_number}. Response: {response}")
        return response
    except Exception as e:
        logger.error(f"Failed to send SMS: {e}")
        raise e
