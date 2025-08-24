from fastapi import APIRouter, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse, HTMLResponse
from datetime import datetime
from typing import Dict
import os

from ..models import GenerationRequest, GenerationStatus, ProjectInfo
from ..services.page_generator import PageGeneratorService
from ..services.project_manager import ProjectManagerService

router = APIRouter(prefix="/generator", tags=["generator"])

# Initialize services
page_generator = PageGeneratorService()
project_manager = ProjectManagerService()

# In-memory storage for generation status (in production, use Redis or database)
generation_status: Dict[str, GenerationStatus] = {}

@router.get("/", response_class=HTMLResponse, summary="Page Generator UI")
async def generator_ui():
    """Serve the page generator UI"""
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>AI Page Generator</title>
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }

            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                color: #333;
            }

            .container {
                max-width: 800px;
                margin: 0 auto;
                padding: 2rem;
            }

            .header {
                text-align: center;
                margin-bottom: 3rem;
                color: white;
            }

            .header h1 {
                font-size: 3rem;
                margin-bottom: 1rem;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
            }

            .header p {
                font-size: 1.2rem;
                opacity: 0.9;
            }

            .card {
                background: white;
                border-radius: 16px;
                padding: 2rem;
                box-shadow: 0 20px 60px rgba(0,0,0,0.1);
                margin-bottom: 2rem;
            }

            .form-group {
                margin-bottom: 1.5rem;
            }

            label {
                display: block;
                margin-bottom: 0.5rem;
                font-weight: 600;
                color: #333;
            }

            textarea, select {
                width: 100%;
                padding: 12px;
                border: 2px solid #e1e5e9;
                border-radius: 8px;
                font-size: 16px;
                transition: border-color 0.3s;
            }

            textarea {
                min-height: 120px;
                resize: vertical;
            }

            textarea:focus, select:focus {
                outline: none;
                border-color: #667eea;
            }

            .form-row {
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 1rem;
            }

            .btn {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 12px 24px;
                border: none;
                border-radius: 8px;
                font-size: 16px;
                font-weight: 600;
                cursor: pointer;
                transition: transform 0.2s;
                width: 100%;
            }

            .btn:hover {
                transform: translateY(-2px);
            }

            .btn:disabled {
                opacity: 0.6;
                cursor: not-allowed;
                transform: none;
            }

            .progress-container {
                display: none;
                margin-top: 2rem;
            }

            .progress-bar {
                width: 100%;
                height: 8px;
                background: #e1e5e9;
                border-radius: 4px;
                overflow: hidden;
            }

            .progress-fill {
                height: 100%;
                background: linear-gradient(90deg, #667eea, #764ba2);
                border-radius: 4px;
                transition: width 0.3s;
                width: 0%;
            }

            .progress-text {
                text-align: center;
                margin-top: 1rem;
                font-weight: 600;
            }

            .result-container {
                display: none;
                margin-top: 2rem;
            }

            .download-btn {
                background: #10b981;
                margin-top: 1rem;
            }

            .projects-section {
                margin-top: 3rem;
            }

            .project-item {
                background: rgba(255,255,255,0.1);
                border-radius: 12px;
                padding: 1.5rem;
                margin-bottom: 1rem;
                color: white;
                display: flex;
                justify-content: space-between;
                align-items: center;
            }

            .project-info h3 {
                margin-bottom: 0.5rem;
            }

            .project-meta {
                font-size: 0.9rem;
                opacity: 0.8;
            }

            .project-actions {
                display: flex;
                gap: 0.5rem;
            }

            .btn-small {
                padding: 6px 12px;
                font-size: 14px;
                background: rgba(255,255,255,0.2);
                border: 1px solid rgba(255,255,255,0.3);
            }

            @media (max-width: 768px) {
                .container {
                    padding: 1rem;
                }
                
                .header h1 {
                    font-size: 2rem;
                }
                
                .form-row {
                    grid-template-columns: 1fr;
                }
                
                .project-item {
                    flex-direction: column;
                    align-items: flex-start;
                    gap: 1rem;
                }
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🎨 AI Page Generator</h1>
                <p>Generate modern web applications with AI</p>
            </div>

            <div class="card">
                <form id="generateForm">
                    <div class="form-group">
                        <label for="userPrompt">What do you want to build?</label>
                        <textarea 
                            id="userPrompt" 
                            name="userPrompt" 
                            placeholder="Describe your web application... (e.g., A modern e-commerce store for books with search, cart, and user profiles)"
                            required
                        ></textarea>
                    </div>

                    <div class="form-row">
                        <div class="form-group">
                            <label for="framework">Framework</label>
                            <select id="framework" name="framework">
                                <option value="React">React</option>
                                <option value="Vue">Vue</option>
                            </select>
                        </div>

                        <div class="form-group">
                            <label for="language">Language</label>
                            <select id="language" name="language">
                                <option value="JS">JavaScript</option>
                                <option value="TS">TypeScript</option>
                            </select>
                        </div>
                    </div>

                    <div class="form-row">
                        <div class="form-group">
                            <label for="model">AI Model</label>
                            <select id="model" name="model">
                                <option value="gpt-4o">GPT-4o (Best Quality)</option>
                                <option value="gpt-4-turbo">GPT-4 Turbo (Good Balance)</option>
                                <option value="gpt-3.5-turbo">GPT-3.5 Turbo (Most Economical)</option>
                            </select>
                        </div>

                        <div class="form-group">
                            <label for="costOptimization">
                                <input type="checkbox" id="costOptimization" name="costOptimization">
                                Cost Optimization (Fewer pages)
                            </label>
                        </div>
                    </div>

                    <button type="submit" class="btn" id="generateBtn">
                        ✨ Generate Project
                    </button>
                </form>

                <div class="progress-container" id="progressContainer">
                    <div class="progress-bar">
                        <div class="progress-fill" id="progressFill"></div>
                    </div>
                    <div class="progress-text" id="progressText">Starting generation...</div>
                </div>

                <div class="result-container" id="resultContainer">
                    <h3>🎉 Project Generated Successfully!</h3>
                    <p>Your project has been generated and packaged.</p>
                    <button class="btn download-btn" id="downloadBtn">
                        📥 Download Project
                    </button>
                </div>
            </div>

            <div class="projects-section">
                <div class="card">
                    <h2>📂 Generated Projects</h2>
                    <div id="projectsList">
                        <p>Loading projects...</p>
                    </div>
                </div>
            </div>
        </div>

        <script>
            let currentGenerationId = null;
            let statusInterval = null;

            // Load projects on page load
            document.addEventListener('DOMContentLoaded', loadProjects);

            // Handle form submission
            document.getElementById('generateForm').addEventListener('submit', async (e) => {
                e.preventDefault();
                
                const formData = new FormData(e.target);
                const data = {
                    user_prompt: formData.get('userPrompt'),
                    framework: formData.get('framework'),
                    language: formData.get('language'),
                    model: formData.get('model'),
                    cost_optimization: formData.has('costOptimization')
                };

                try {
                    // Show progress
                    document.getElementById('progressContainer').style.display = 'block';
                    document.getElementById('resultContainer').style.display = 'none';
                    document.getElementById('generateBtn').disabled = true;
                    document.getElementById('generateBtn').textContent = 'Generating...';

                    // Start generation
                    const response = await fetch('/generator/generate', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify(data)
                    });

                    const result = await response.json();
                    currentGenerationId = result.generation_id;

                    // Start polling for status
                    statusInterval = setInterval(checkStatus, 2000);

                } catch (error) {
                    console.error('Error:', error);
                    alert('Failed to start generation. Please check your configuration.');
                    resetUI();
                }
            });

            async function checkStatus() {
                if (!currentGenerationId) return;

                try {
                    const response = await fetch(`/generator/status/${currentGenerationId}`);
                    const status = await response.json();

                    // Update progress
                    document.getElementById('progressFill').style.width = `${status.progress}%`;
                    document.getElementById('progressText').textContent = status.message;

                    if (status.status === 'completed') {
                        clearInterval(statusInterval);
                        showCompleted(status.project_info);
                        loadProjects(); // Refresh projects list
                    } else if (status.status === 'failed') {
                        clearInterval(statusInterval);
                        alert(`Generation failed: ${status.error}`);
                        resetUI();
                    }

                } catch (error) {
                    console.error('Error checking status:', error);
                }
            }

            function showCompleted(projectInfo) {
                document.getElementById('progressContainer').style.display = 'none';
                document.getElementById('resultContainer').style.display = 'block';
                
                const downloadBtn = document.getElementById('downloadBtn');
                downloadBtn.onclick = () => {
                    window.location.href = projectInfo.download_url.replace('/download/', '/generator/download/');
                };

                resetUI();
            }

            function resetUI() {
                document.getElementById('generateBtn').disabled = false;
                document.getElementById('generateBtn').textContent = '✨ Generate Project';
            }

            async function loadProjects() {
                try {
                    const response = await fetch('/generator/projects');
                    const projects = await response.json();
                    
                    const container = document.getElementById('projectsList');
                    
                    if (projects.length === 0) {
                        container.innerHTML = '<p>No projects generated yet.</p>';
                        return;
                    }

                    container.innerHTML = projects.map(project => `
                        <div class="project-item">
                            <div class="project-info">
                                <h3>${project.name}</h3>
                                <div class="project-meta">
                                    ${project.framework} ${project.language} • 
                                    ${project.pages_count} pages • 
                                    ${project.size_mb}MB • 
                                    ${new Date(project.created_at).toLocaleDateString()}
                                </div>
                            </div>
                            <div class="project-actions">
                                <button class="btn btn-small" onclick="downloadProject('${project.id}')">
                                    📥 Download
                                </button>
                                <button class="btn btn-small" onclick="deleteProject('${project.id}')" style="background: rgba(239, 68, 68, 0.2);">
                                    🗑️ Delete
                                </button>
                            </div>
                        </div>
                    `).join('');

                } catch (error) {
                    console.error('Error loading projects:', error);
                    document.getElementById('projectsList').innerHTML = '<p>Error loading projects.</p>';
                }
            }

            function downloadProject(projectId) {
                window.location.href = `/generator/download/${projectId}`;
            }

            async function deleteProject(projectId) {
                if (!confirm('Are you sure you want to delete this project?')) return;

                try {
                    const response = await fetch(`/generator/projects/${projectId}`, {
                        method: 'DELETE'
                    });

                    if (response.ok) {
                        loadProjects(); // Refresh list
                    } else {
                        alert('Failed to delete project');
                    }
                } catch (error) {
                    console.error('Error deleting project:', error);
                    alert('Error deleting project');
                }
            }
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

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

async def generate_pages_background(generation_id: str, request: GenerationRequest):
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
