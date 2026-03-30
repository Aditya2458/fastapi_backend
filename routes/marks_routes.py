from fastapi import APIRouter, Depends
from schemas import MarkCreate
from crud import create_mark, get_marks
from dependencies import require_role
from fastapi import HTTPException
from services.marks_service import add_mark_service, list_marks_service


router = APIRouter(prefix="/api/marks", tags=["Marks"])


from crud import is_teacher_assigned
from fastapi import APIRouter, Depends, HTTPException
from schemas import MarkCreate
from dependencies import require_role
from crud import is_teacher_assigned
from services.marks_service import add_mark_service, list_marks_service

router = APIRouter(prefix="/api/marks", tags=["Marks"])

@router.post("/")
def add_mark(mark: MarkCreate, current_user=Depends(require_role("teacher"))):

    teacher_id = int(current_user["sub"])

    success = add_mark_service(mark, teacher_id)

    if not success:
        raise HTTPException(status_code=403, detail="Not allowed for this subject")

    return {"message": "Marks added"}

@router.get("/")
def list_marks():
    return list_marks_service()