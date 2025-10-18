from dotenv import load_dotenv
import os

load_dotenv()  

class Settings:
       REST_API_URL = os.getenv("REST_API_URL")
settings = Settings()