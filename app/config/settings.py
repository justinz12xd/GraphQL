from dotenv import load_dotenv
import os

load_dotenv()  

class Settings:
    """Configuración de la aplicación"""
    REST_API_URL = os.getenv("REST_API_URL", "http://localhost:8080")
    GRAPHQL_HOST = os.getenv("GRAPHQL_HOST", "0.0.0.0")
    GRAPHQL_PORT = int(os.getenv("GRAPHQL_PORT", "4000"))
    DEBUG = os.getenv("DEBUG", "True").lower() == "true"
    HTTP_TIMEOUT = int(os.getenv("HTTP_TIMEOUT", "30"))

settings = Settings()
