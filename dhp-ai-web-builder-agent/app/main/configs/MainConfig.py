import os
import dotenv

dotenv.load_dotenv()

SA_CONNECTION = os.environ.get("SA_CONNECTION") 
SA_SHARE_NAME = os.environ.get("SA_SHARE_NAME") or "file-search-image-dev"
