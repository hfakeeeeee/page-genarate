import subprocess
from azure.storage.fileshare import ShareFileClient
from fastapi import APIRouter

from app.main.configs import MainConfig

router = APIRouter()


class ProcessService:

    def __init__(self):
        self.__connection_string = MainConfig.SA_CONNECTION
        self.__share_name = MainConfig.SA_SHARE_NAME

    def download_file(self, file_path, local_path):
        connection_string = self.__connection_string
        share_name = self.__share_name

        file_client = ShareFileClient.from_connection_string(
            conn_str=connection_string, share_name=share_name, file_path=file_path
        )

        with open(local_path, "wb") as file_handle:
            data = file_client.download_file()
            file_handle.write(data.readall())

        print(f"File downloaded to {local_path}")

    def launch_project(self, request_body):
        file_path = request_body.file_path
        live_preview_port = request_body.live_preview_port
        live_preview_path = request_body.live_preview_path

        local_path = f"projects/{file_path.split('/')[-1]}"

        self.download_file(file_path, local_path)

        params = [
            file_path.split("/")[-1].replace(".zip", ""),
            str(live_preview_port),
            live_preview_path,
        ]

        command = ["bash", "./start_vite.sh"] + params
        subprocess.Popen(command)

        return {"message": "Project launched successfully"}

    def stop_project(self, request_body):
        params = [str(request_body.pid)]

        subprocess.Popen(["bash", "-c", f'{"./kill_process.sh"} {" ".join(params)}'])

        return {"message": "Project stopped successfully"}
