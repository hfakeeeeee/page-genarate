from fastapi import APIRouter, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse
from datetime import datetime
from typing import Dict
import os

from app.models import GenerationRequest, GenerationStatus
from app.services.page_generator import PageGeneratorService
from app.services.project_manager import ProjectManagerService

router = APIRouter(prefix="/generator", tags=["generator"])

# Initialize services
page_generator = PageGeneratorService()
project_manager = ProjectManagerService()

# In-memory storage for generation status
generation_status: Dict[str, GenerationStatus] = {}


@router.post("/generate", summary="Start page generation")
async def generate_pages(
    request: GenerationRequest,
    background_tasks: BackgroundTasks
):
    """Start page generation process"""
    generation_id = f"gen_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

    # Initialize status
    generation_status[generation_id] = GenerationStatus(
        id=generation_id,
        status="starting",
        progress=0,
        message="Initializing generation...",
        created_at=datetime.now()
    )

    # Start background generation
    background_tasks.add_task(
        generate_pages_background,
        generation_id,
        request
    )

    return {"generation_id": generation_id, "message": "Generation started"}


@router.get("/status/{generation_id}", summary="Get generation status")
async def get_generation_status(generation_id: str):
    """Get generation status"""
    if generation_id not in generation_status:
        raise HTTPException(status_code=404, detail="Generation not found")

    return generation_status[generation_id]


@router.get("/projects", summary="List generated projects")
async def list_projects():
    """List all generated projects"""
    return await project_manager.list_projects()


@router.get("/download/{project_id}", summary="Download project")
async def download_project(project_id: str):
    """Download project as zip file"""
    zip_path = await project_manager.get_project_zip(project_id)
    if not zip_path or not os.path.exists(zip_path):
        raise HTTPException(status_code=404, detail="Project not found")

    return FileResponse(
        zip_path,
        media_type="application/zip",
        filename=f"{project_id}.zip"
    )


@router.delete("/projects/{project_id}", summary="Delete project")
async def delete_project(project_id: str):
    """Delete a generated project"""
    success = await project_manager.delete_project(project_id)
    if not success:
        raise HTTPException(status_code=404, detail="Project not found")

    return {"message": "Project deleted successfully"}


async def generate_pages_background(generation_id: str,
                                    request: GenerationRequest):
    """Background task for page generation"""
    try:
        status = generation_status[generation_id]

        # Step 1: Generate project plan
        status.status = "planning"
        status.progress = 10
        status.message = "Creating project plan..."

        project_plan = await page_generator.generate_project_plan(
            request.user_prompt,
            request.framework,
            request.language
        )

        # Step 2: Generate pages
        status.status = "generating"
        status.progress = 30
        status.message = "Generating pages..."

        pages_result = await page_generator.generate_pages(
            project_plan,
            progress_callback=lambda p, m: update_progress(generation_id, p, m)
        )

        # Step 3: Generate router
        status.status = "routing"
        status.progress = 80
        status.message = "Creating router..."

        router_result = await page_generator.generate_router(project_plan)

        # Step 4: Package project
        status.status = "packaging"
        status.progress = 90
        status.message = "Packaging project..."

        project_info = await project_manager.package_project(
            generation_id,
            project_plan,
            pages_result,
            router_result
        )

        # Complete
        status.status = "completed"
        status.progress = 100
        status.message = "Generation completed successfully!"
        status.project_info = project_info

    except Exception as e:
        status.status = "failed"
        status.message = f"Generation failed: {str(e)}"
        status.error = str(e)


def update_progress(generation_id: str, progress: int, message: str):
    """Update generation progress"""
    if generation_id in generation_status:
        generation_status[generation_id].progress = progress
        generation_status[generation_id].message = message
