from fastapi import APIRouter, Depends
from schemas import CreateClass
from crud import create_class
from dependencies import require_role

router = APIRouter(prefix="/api/classes", tags=["Classes"])

@router.post("/")
def create_new_class(data: CreateClass,_=Depends(require_role("admin"))):
    class_id = create_class(data.name, data.section)
    return {
        "message": "Class created successfully",
        "class_id": class_id
    }