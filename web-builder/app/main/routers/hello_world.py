from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/hello", tags=["hello"])


class GreetRequest(BaseModel):
    name: str = "world"


@router.get("", summary="Greet")
def hello(name: str = "world"):
    return {"message": f"Hello, {name}"}


@router.get("/{name}", summary="Greet with path")
def hello_with_path(name: str):
    return {"message": f"Hello, {name}"}


@router.post("", summary="Greet with body")
def hello_with_body(request: GreetRequest):
    return {"message": f"Hello, {request.name}"}
