import os

from dotenv import load_dotenv

load_dotenv()

user_name = os.getenv('user_name', 'USER_NAME')
access_key = os.getenv('access_key', 'ACCESS_KEY')
driver_remote_url = os.getenv('driver_remote_ur', 'DRIVER_REMOTE_URL')