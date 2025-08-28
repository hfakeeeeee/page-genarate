import os
import dotenv

dotenv.load_dotenv()

SA_CONNECTION = os.environ.get("SA_CONNECTION")
SA_SHARE_NAME = os.environ.get("SA_SHARE_NAME")


class Settings:
    # Azure OpenAI Configuration (following notebook logic)
    AZURE_ENDPOINT: str = os.getenv("AZURE_ENDPOINT")
    AZURE_MODEL: str = os.getenv("AZURE_MODEL")
    AZURE_API_VERSION: str = os.getenv("AZURE_API_VERSION")
    AZURE_OPENAI_API_KEY: str = os.getenv("AZURE_OPENAI_API_KEY")

    # Paths
    OUTPUT_PATH: str = os.getenv("OUTPUT_PATH")
    BASE_PROJECTS_PATH: str = os.getenv("BASE_PROJECTS_PATH")
    PROMPTS_PATH: str = os.getenv("PROMPTS_PATH")
    SA_CONNECTION: str = os.getenv("SA_CONNECTION")
    SA_SHARE_NAME: str = os.getenv("SA_SHARE_NAME")

    def __init__(self):
        # Ensure output directory exists
        os.makedirs(self.OUTPUT_PATH, exist_ok=True)

        # Validate Azure OpenAI API key (primary)
        if not self.AZURE_OPENAI_API_KEY:
            print("AZURE_OPENAI_API_KEY not set")


settings = Settings()
