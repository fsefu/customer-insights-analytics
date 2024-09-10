import os
from dotenv import load_dotenv

def load_environment():
    """
    Load environment variables from a .env file into the system environment.
    """
    env_file = os.path.join(os.getcwd(), '.env')
    
    if os.path.exists(env_file):
        load_dotenv(env_file)
        print("Environment variables loaded successfully from .env file.")
    else:
        raise FileNotFoundError(f"The .env file could not be found at {env_file}.")
