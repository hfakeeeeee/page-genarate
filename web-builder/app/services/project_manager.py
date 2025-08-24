import os
import json
import shutil
import zipfile
from datetime import datetime
from typing import List, Dict, Optional
from pathlib import Path

from ..config import settings
from ..models import ProjectPlan, ProjectInfo

class ProjectManagerService:
    def __init__(self):
        self.output_path = Path(settings.OUTPUT_PATH)
        self.base_projects_path = Path(settings.BASE_PROJECTS_PATH)
        
        # Ensure output directories exist
        self.output_path.mkdir(exist_ok=True)
        (self.output_path / "projects").mkdir(exist_ok=True)
        (self.output_path / "zips").mkdir(exist_ok=True)
    
    async def package_project(
        self,
        generation_id: str,
        project_plan: ProjectPlan,
        pages: Dict[str, str],
        router_code: str
    ) -> ProjectInfo:
        """Package the generated project into a complete structure"""
        
        # Create project directory
        project_dir = self.output_path / "projects" / generation_id
        if project_dir.exists():
            shutil.rmtree(project_dir)
        
        # Copy base project template
        await self._copy_base_project(project_plan.framework, project_plan.language, project_dir)
        
        # Write generated pages
        pages_dir = project_dir / "src" / "pages"
        pages_dir.mkdir(parents=True, exist_ok=True)
        
        for filepath, code in pages.items():
            file_path = project_dir / filepath
            file_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(code)
        
        # Write router
        router_path = project_dir / "src" / "App.jsx"
        if project_plan.language == "TS":
            router_path = project_dir / "src" / "App.tsx"
        
        with open(router_path, "w", encoding="utf-8") as f:
            f.write(router_code)
        
        # Create project info file
        project_info_data = {
            "id": generation_id,
            "name": project_plan.project_name,
            "framework": project_plan.framework,
            "language": project_plan.language,
            "description": project_plan.description,
            "pages": [page.model_dump() for page in project_plan.pages],
            "created_at": datetime.now().isoformat()
        }
        
        with open(project_dir / "project-info.json", "w", encoding="utf-8") as f:
            json.dump(project_info_data, f, indent=2)
        
        # Create zip file
        zip_path = await self._create_zip(project_dir, generation_id)
        
        # Calculate size
        size_mb = round(os.path.getsize(zip_path) / (1024 * 1024), 2)
        
        return ProjectInfo(
            id=generation_id,
            name=project_plan.project_name,
            framework=project_plan.framework,
            language=project_plan.language,
            pages_count=len(project_plan.pages),
            created_at=datetime.now(),
            download_url=f"/download/{generation_id}",
            size_mb=size_mb
        )
    
    async def list_projects(self) -> List[ProjectInfo]:
        """List all generated projects"""
        projects = []
        projects_dir = self.output_path / "projects"
        
        if not projects_dir.exists():
            return projects
        
        for project_dir in projects_dir.iterdir():
            if project_dir.is_dir():
                info_file = project_dir / "project-info.json"
                if info_file.exists():
                    try:
                        with open(info_file, "r", encoding="utf-8") as f:
                            data = json.load(f)
                        
                        projects.append(ProjectInfo(
                            id=data["id"],
                            name=data["name"],
                            framework=data["framework"],
                            language=data["language"],
                            pages_count=len(data.get("pages", [])),
                            created_at=datetime.fromisoformat(data["created_at"]),
                            download_url=f"/download/{data['id']}",
                            size_mb=await self._get_zip_size(data["id"])
                        ))
                    except Exception as e:
                        print(f"Error reading project info for {project_dir.name}: {e}")
        
        # Sort by creation date, newest first
        projects.sort(key=lambda x: x.created_at, reverse=True)
        return projects
    
    async def get_project_zip(self, project_id: str) -> Optional[str]:
        """Get path to project zip file"""
        zip_path = self.output_path / "zips" / f"{project_id}.zip"
        if zip_path.exists():
            return str(zip_path)
        return None
    
    async def delete_project(self, project_id: str) -> bool:
        """Delete a project and its zip file"""
        try:
            # Delete project directory
            project_dir = self.output_path / "projects" / project_id
            if project_dir.exists():
                shutil.rmtree(project_dir)
            
            # Delete zip file
            zip_path = self.output_path / "zips" / f"{project_id}.zip"
            if zip_path.exists():
                zip_path.unlink()
            
            return True
        except Exception as e:
            print(f"Error deleting project {project_id}: {e}")
            return False
    
    async def _copy_base_project(self, framework: str, language: str, destination: Path):
        """Copy the appropriate base project template"""
        framework = framework.lower()
        language = language.lower()
        
        # Determine source directory
        if framework == "react":
            if language == "ts":
                source_dir = self.base_projects_path / "react-ts"
            else:
                source_dir = self.base_projects_path / "react-js"
        elif framework == "vue":
            if language == "ts":
                source_dir = self.base_projects_path / "vue-ts"
            else:
                source_dir = self.base_projects_path / "vue-js"
        else:
            raise ValueError(f"Unsupported framework: {framework}")
        
        if not source_dir.exists():
            raise FileNotFoundError(f"Base project not found: {source_dir}")
        
        # Copy the base project
        shutil.copytree(source_dir, destination)
    
    async def _create_zip(self, project_dir: Path, project_id: str) -> str:
        """Create a zip file of the project"""
        zip_path = self.output_path / "zips" / f"{project_id}.zip"
        
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for file_path in project_dir.rglob('*'):
                if file_path.is_file():
                    # Skip certain files
                    if file_path.name in ['.DS_Store', 'Thumbs.db', '.git']:
                        continue
                    
                    arcname = file_path.relative_to(project_dir)
                    zipf.write(file_path, arcname)
        
        return str(zip_path)
    
    async def _get_zip_size(self, project_id: str) -> Optional[float]:
        """Get size of zip file in MB"""
        zip_path = self.output_path / "zips" / f"{project_id}.zip"
        if zip_path.exists():
            return round(os.path.getsize(zip_path) / (1024 * 1024), 2)
        return None
