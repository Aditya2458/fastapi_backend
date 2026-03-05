from fastapi import APIRouter, Depends
from crud import create_subject, get_subjects
from schemas import SubjectCreate
from dependencies import require_role

router = APIRouter(prefix="/api/subjects", tags=["Subjects"])


@router.post("/")
def add_subject(subject: SubjectCreate, current_user=Depends(require_role("admin"))):
    create_subject(subject.name, subject.code)
    return {"message": "Subject created"}


@router.get("/")
def list_subjects():
    return get_subjects()