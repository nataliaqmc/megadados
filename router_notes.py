
from fastapi import HTTPException, APIRouter
from fastapi.params import Body, Path, Depends
from typing import List
from schemas import AddNote, Note

from sqlalchemy.orm.session import Session

# substituir ao implementar a conexao com o banco de dados
# from utils import dummy_database as db

from database import get_db
import crud

router = APIRouter(prefix='/note', tags=['notes'])


@router.post('/{subject_id}', response_model=List[Note])
async def add_note(
    subject_id: int = Path(
        ...,
        example=3
    ),
    body: AddNote = Body(
        ...,
        example={"note": 5}
    ),
    db: Session = Depends(get_db)
):

    db_subject = crud.find_subject_by_id(db, subject_id=subject_id)
    
    # subject_exists = db.has(str(subject_id))

    if not db_subject:
        raise HTTPException(
            404, detail=f"Subject with id '{subject_id}' does not exist")

    subject_note = crud.create_subject_note(db, note = body.note, subject_id =subject_id)

    return subject_note


@router.delete('/{subject_id}/{note_id}', response_model=None)
async def delete_note(
        subject_id: int = Path(
            ...,
            example=3
        ),
        note_id: int = Path(
            ...,
            example=3
        ),
        db: Session = Depends(get_db)):

    # subject_exists = db.has(str(subject_id))

    old_subject = crud.find_subject_by_id(db, subject_id)

    old_note = crud.find_note_by_id(db, note_id)

    if not old_subject:
        raise HTTPException(
            404, detail=f"Subject with id '{subject_id}' does not exist")

    # note_exists = db.has_note(str(subject_id), str(note_id))
    if not old_note:
        raise HTTPException(
            404, detail=f"Note with id '{note_id}' does not exist in the subject with id '{subject_id}'")

    crud.delete_note_by_id(db, note_id=note_id)


@router.get('/{subject_id}', response_model=List[Note])
async def list_notes(
        subject_id: int = Path(
            ...,
            example=3
        ),
        skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):

    # subject = db.find_by_id(str(subject_id))
    old_subject = crud.find_subject_by_id(db, subject_id)

    if not old_subject:
        raise HTTPException(
            404, detail=f"Subject with id '{subject_id}' does not exist")

    return old_subject['notes']


@router.patch('/{subject_id}/{note_id}', response_model=List[Note])
async def update_note(
        subject_id: int = Path(
            ...,
            example=int
        ),
        note_id: int = Path(
            ...,
            example=int
        ),
        data: AddNote = Body(
            ...,
            example={'note': 5.6}
        ),
        db: Session = Depends(get_db)):

    # subject_exists = db.has(str(subject_id))

    old_subject = crud.find_subject_by_id(db, subject_id)

    old_note = crud.find_note_by_id(db, note_id)

    if not old_subject:
        raise HTTPException(
            404, detail=f"Subject with id '{subject_id}' does not exist")

    # note_exists = db.has_note(str(subject_id), str(note_id))
    if not old_note:
        raise HTTPException(
            404, detail=f"Note with id '{note_id}' does not exist in the subject with id '{subject_id}'")

    new = crud.update_subject_by_id(db,note_id = note_id, note = data.dict())

    return new
