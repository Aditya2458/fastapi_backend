from fastapi import APIRouter, Depends, HTTPException
from schemas import TeacherSubjectCreate
from crud import assign_teacher_subject
from dependencies import require_role


router = APIRouter(prefix="/api/teacher-subjects", tags=["Teacher-Subjects"])


@router.post("/")
def assign(data: TeacherSubjectCreate, current_user=Depends(require_role("admin"))):
    assign_teacher_subject(data.teacher_id, data.subject_id)
    return {"message": "Teacher assigned to subject"}