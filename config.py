import urllib.parse
from dotenv import load_dotenv
import os

# Tải các biến môi trường từ file .env
load_dotenv()

# Mã hóa thông tin kết nối
username = urllib.parse.quote_plus('root')
password = urllib.parse.quote_plus('Viet211003@s')
hostname = 'localhost'
database = 'facereg'

class Config:
    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{username}:{password}@{hostname}/{database}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY', 'your_secret_key')
