import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Settings:
    # OpenAI Configuration
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    MODEL: str = os.getenv("MODEL", "gpt-4o")
    
    # Paths
    OUTPUT_PATH: str = os.getenv("OUTPUT_PATH", "./output")
    BASE_PROJECTS_PATH: str = os.getenv("BASE_PROJECTS_PATH", "./base_projects")
    PROMPTS_PATH: str = os.getenv("PROMPTS_PATH", "./prompts")
    
    def __init__(self):
        # Ensure output directory exists
        os.makedirs(self.OUTPUT_PATH, exist_ok=True)
        
        # Validate OpenAI API key
        if not self.OPENAI_API_KEY:
            print("⚠️ Warning: OPENAI_API_KEY not set. Please configure it in environment variables")

settings = Settings()
