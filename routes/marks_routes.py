from fastapi import APIRouter, Depends
from schemas import MarkCreate
from crud import create_mark, get_marks
from dependencies import require_role

router = APIRouter(prefix="/api/marks", tags=["Marks"])


@router.post("/")
def add_mark(mark: MarkCreate, current_user=Depends(require_role("teacher"))):
    create_mark(mark.student_id, mark.subject_id, mark.exam_type, mark.marks)
    return {"message": "Marks added"}


@router.get("/")
def list_marks():
    return get_marks()