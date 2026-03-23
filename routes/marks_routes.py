from fastapi import APIRouter, Depends
from schemas import MarkCreate
from crud import create_mark, get_marks
from dependencies import require_role
from fastapi import HTTPException

router = APIRouter(prefix="/api/marks", tags=["Marks"])


from crud import is_teacher_assigned

@router.post("/")
def add_mark(mark: MarkCreate, current_user=Depends(require_role("teacher"))):

    teacher_id = int(current_user["sub"])

    assigned = is_teacher_assigned(teacher_id, mark.subject_id)

    if not assigned:
        raise HTTPException(status_code=403, detail="Not allowed for this subject")

    create_mark(mark.student_id, mark.subject_id, mark.exam_type, mark.marks)

    return {"message": "Marks added"}


@router.get("/")
def list_marks():
    return get_marks()