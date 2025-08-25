from pydantic import BaseModel, Field


class SimpleGenerationRequest(BaseModel):
    description: str = Field(..., description="Simple description of what you want to build")


class SimpleProjectResult(BaseModel):
    project_name: str
    framework: str
    language: str
    files: dict  # filename -> content mapping
    description: str
