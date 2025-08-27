import os
import dotenv

dotenv.load_dotenv()

SA_CONNECTION = os.environ.get("SA_CONNECTION") or "DefaultEndpointsProtocol=https;AccountName=dhp0search0npe;AccountKey=vOdji7Zrhe/3HAUcdTkhClWie9+e8JM6HPyGmXXxGGtEAMvtMiIlgL0HlAfOYPheLxyzMv8qTUU/+AStfhtoYw==;EndpointSuffix=core.windows.net"
SA_SHARE_NAME = os.environ.get("SA_SHARE_NAME") or "file-search-image-dev"
