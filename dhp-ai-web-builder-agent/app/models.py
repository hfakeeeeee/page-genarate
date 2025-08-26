from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum


class ReactLanguage(str, Enum):
    JAVASCRIPT = "JavaScript"
    TYPESCRIPT = "TypeScript"


class SimpleGenerationRequest(BaseModel):
    description: str = Field(..., description="Description of what you want to build")
    framework: str = Field(default="React", description="Frontend framework (React only)")
    language: ReactLanguage = Field(default=ReactLanguage.JAVASCRIPT, description="Programming language (JavaScript or TypeScript)")
    
    class Config:
        use_enum_values = True


class SimpleProjectResult(BaseModel):
    project_name: str
    framework: str
    language: str
    files: dict  # filename -> content mapping
    description: str


class Framework(str, Enum):
    REACT = "React"
    VUE = "Vue"


class Language(str, Enum):
    JS = "JS"
    TS = "TS"


class GenerationRequest(BaseModel):
    user_prompt: str = Field(...,
                             description="User's description")
    framework: Framework = Field(default=Framework.REACT,
                                 description="Frontend framework")
    language: Language = Field(default=Language.JS,
                               description="Programming language")


class GenerationStatus(BaseModel):
    id: str
    # starting, planning, generating, routing, packaging, completed, failed
    status: str
    progress: int = Field(default=0, ge=0, le=100)
    message: str = ""
    error: Optional[str] = None
    created_at: datetime
    completed_at: Optional[datetime] = None
    project_info: Optional['ProjectInfo'] = None


class ProjectInfo(BaseModel):
    id: str
    name: str
    framework: str
    language: str
    pages_count: int
    created_at: datetime
    download_url: str
    size_mb: Optional[float] = None


class PageInfo(BaseModel):
    name: str
    filepath: str
    route: str
    description: str
    generated: bool = False
    error: Optional[str] = None


class ProjectPlan(BaseModel):
    framework: str
    language: str
    project_name: str
    description: str
    pages: List[PageInfo]


# Update forward reference
GenerationStatus.model_rebuild()
