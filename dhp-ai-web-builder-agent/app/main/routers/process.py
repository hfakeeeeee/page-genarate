from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional

from app.main.services.process import ProcessService


router = APIRouter(prefix="/v1/process", tags=["process"])
process_service = ProcessService()


class CreateLaunchProjectDTO(BaseModel):
    file_path: Optional[str] = None
    live_preview_port: Optional[int] = None
    live_preview_path: Optional[str] = None


class CreateStopProjectDTO(BaseModel):
    pid: Optional[int] = None


@router.post("/launch", summary="Launch a Project")
def launch_project(request_body: CreateLaunchProjectDTO):
    process_service.launch_project(request_body)
    return {"message": "Project launched successfully"}


@router.post("/stop", summary="Stop a Project")
def launch_project(request_body: CreateStopProjectDTO):
    process_service.stop_project(request_body)
    return {"message": "Project stopped successfully"}
