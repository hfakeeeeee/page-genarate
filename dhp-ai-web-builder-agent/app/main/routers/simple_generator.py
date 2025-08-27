from fastapi import APIRouter, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse
from datetime import datetime
from typing import Dict
import os

from app.models import SimpleGenerationRequest, GenerationStatus
from app.services.simple_generator import SimpleGeneratorService
from app.services.project_manager import ProjectManagerService

router = APIRouter(prefix="/simple-generator", tags=["simple-generator"])

# Initialize services
simple_generator = SimpleGeneratorService()
project_manager = ProjectManagerService()

# In-memory storage for generation status
generation_status: Dict[str, GenerationStatus] = {}


@router.post("/generate", summary="Generate React project with AI")
async def generate_project_freely(
    request: SimpleGenerationRequest
):
    """
    Generate a complete React project with AI assistance.

    The AI will create a full React application based on your description,
    using either JavaScript or TypeScript as specified.

    Input:
    - description: What you want to build
    - framework: React (fixed)
    - language: JavaScript or TypeScript

    The AI will handle:
    - Project structure and architecture
    - Component design and implementation
    - Styling and responsive design
    - Modern React patterns and best practices
    - Complete working application with all necessary files
    """
    generation_id = f"simple_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

    # Initialize status
    generation_status[generation_id] = GenerationStatus(
        id=generation_id,
        status="starting",
        progress=0,
        message=f"AI is preparing to create your React ({request.language}) project...",
        created_at=datetime.now()
    )

    # Start background generation
    response = await generate_project_background(generation_id, request)
    print(response)

    return response.project_info.__dict__


@router.get("/status/{generation_id}", summary="Get generation status")
async def get_generation_status(generation_id: str):
    """Get generation status"""
    if generation_id not in generation_status:
        raise HTTPException(status_code=404, detail="Generation not found")

    return generation_status[generation_id]


@router.get("/download/{generation_id}", summary="Download generated project")
async def download_project(generation_id: str):
    """Download project as zip file"""
    if generation_id not in generation_status:
        raise HTTPException(status_code=404, detail="Generation not found")

    status = generation_status[generation_id]
    if status.status != "completed" or not status.project_info:
        raise HTTPException(status_code=400, detail="Project not ready for download")

    zip_path = await project_manager.get_project_zip(status.project_info.id)
    if not zip_path or not os.path.exists(zip_path):
        raise HTTPException(status_code=404, detail="Project file not found")

    return FileResponse(
        zip_path,
        media_type="application/zip",
        filename=f"{generation_id}.zip"
    )


async def generate_project_background(generation_id: str, request: SimpleGenerationRequest):
    """Background task for free-form project generation"""
    try:
        status = generation_status[generation_id]

        # Update status
        status.status = "generating"
        status.progress = 50
        status.message = f"AI is designing and building your React ({request.language}) project..."

        # Generate complete project with AI freedom
        project_result = await simple_generator.generate_complete_project(
            request.description,
            request.framework,
            request.language,
            progress_callback=lambda p, m: update_progress(generation_id, p, m)
        )

        # Package the project
        status.status = "packaging"
        status.progress = 90
        status.message = "Finalizing project..."

        project_info = await project_manager.package_simple_project(
            generation_id,
            project_result
        )

        # Complete
        status.status = "completed"
        status.progress = 100
        status.message = "Project created successfully!"
        status.project_info = project_info

    except Exception as e:
        status.status = "failed"
        status.message = f"Generation failed: {str(e)}"
        status.error = str(e)
    return status


def update_progress(generation_id: str, progress: int, message: str):
    """Update generation progress"""
    if generation_id in generation_status:
        generation_status[generation_id].progress = progress
        generation_status[generation_id].message = message
