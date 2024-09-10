import os
from dotenv import load_dotenv
import streamlit as st

def load_environment():
    """
    Load environment variables either from a .env file (for local development)
    or from Streamlit secrets (for production).
    """
    if os.getenv('STREAMLIT_ENV') == 'production':
        # Assuming production environment is identified by 'STREAMLIT_ENV' being set to 'production'
        st.secrets["DB_NAME"] = os.getenv("DB_NAME", st.secrets["DB_NAME"])
        st.secrets["DB_HOST"] = os.getenv("DB_HOST", st.secrets["DB_HOST"])
        st.secrets["DB_USER"] = os.getenv("DB_USER", st.secrets["DB_USER"])
        st.secrets["DB_PASSWORD"] = os.getenv("DB_PASSWORD", st.secrets["DB_PASSWORD"])
        st.secrets["DB_PORT"] = os.getenv("DB_PORT", st.secrets["DB_PORT"])
        print("Environment variables loaded from Streamlit secrets (production).")
    else:
        # Load from .env file for local development
        env_file = os.path.join(os.getcwd(), '.env')
        if os.path.exists(env_file):
            load_dotenv(env_file)
            print("Environment variables loaded successfully from .env file (local development).")
        else:
            raise FileNotFoundError(f"The .env file could not be found at {env_file}.")
