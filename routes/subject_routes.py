from fastapi import APIRouter, Depends, HTTPException
from crud import create_subject, get_subjects
from schemas import SubjectCreate
from dependencies import require_role

router = APIRouter(prefix="/api/subjects", tags=["Subjects"])


@router.post("/")
def add_subject(subject: SubjectCreate, current_user=Depends(require_role("admin"))):

    result = create_subject(subject.name, subject.code)

    if isinstance(result, dict) and result.get("status_code") == 409:
        raise HTTPException(status_code=409, detail=result["message"])

    return {"message": "Subject created"}


@router.get("/")
def list_subjects():
    return get_subjects()