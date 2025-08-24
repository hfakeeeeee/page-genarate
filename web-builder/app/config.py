import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Settings:
    # Azure OpenAI Configuration (following notebook logic)
    AZURE_ENDPOINT: str = os.getenv("AZURE_ENDPOINT", "https://dhp-search-east-npe-0.openai.azure.com/")
    AZURE_MODEL: str = os.getenv("AZURE_MODEL", "gpt-4.1")
    AZURE_API_VERSION: str = os.getenv("AZURE_API_VERSION", "2024-02-01")
    AZURE_OPENAI_API_KEY: str = os.getenv("AZURE_OPENAI_API_KEY", "")
    
    # Fallback OpenAI Configuration (for backwards compatibility)
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    MODEL: str = os.getenv("MODEL", "gpt-4o")
    
    # Paths
    OUTPUT_PATH: str = os.getenv("OUTPUT_PATH", "./output")
    BASE_PROJECTS_PATH: str = os.getenv("BASE_PROJECTS_PATH", "./base_projects")
    PROMPTS_PATH: str = os.getenv("PROMPTS_PATH", "./prompts")
    
    def __init__(self):
        # Ensure output directory exists
        os.makedirs(self.OUTPUT_PATH, exist_ok=True)
        
        # Validate Azure OpenAI API key (primary)
        if not self.AZURE_OPENAI_API_KEY:
            print("⚠️ Warning: AZURE_OPENAI_API_KEY not set. Trying fallback OPENAI_API_KEY...")
            if not self.OPENAI_API_KEY:
                print("⚠️ Warning: No API keys configured. Please set AZURE_OPENAI_API_KEY or OPENAI_API_KEY in environment variables")

settings = Settings()
