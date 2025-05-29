import os

from dotenv import load_dotenv

load_dotenv()

user_name = os.getenv('USER_NAME')
access_key = os.getenv('ACCESS_KEY')
driver_remote_url = os.getenv('DRIVER_REMOTE_URL')