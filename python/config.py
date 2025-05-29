from dotenv import load_dotenv
import os

def loadDetails():
    dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
    load_dotenv(dotenv_path)
    return os.getenv("API_USERNAME"), os.getenv("API_PASSWORD"), os.getenv("API_SECRET")