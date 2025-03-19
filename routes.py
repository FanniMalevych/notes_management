from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

import crud
import schemas
from ai_summarize import summarize_note_with_gemini
from analytics import analyze_notes
from db import models
from db.engine import SessionLocal

router = APIRouter()


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/notes/", response_model=list[schemas.Note])
def read_notes(db: Session = Depends(get_db)):
    return crud.get_all_notes(db)


@router.get("/notes/{note_id}/", response_model=schemas.Note)
def read_single_note(note_id: int, db: Session = Depends(get_db)):
    note = crud.get_note(db=db, note_id=note_id)

    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")

    return note


@router.post("/notes/", response_model=schemas.Note)
def create_note(note: schemas.NoteCreate, db: Session = Depends(get_db)):
    return crud.create_note(db=db, note=note)


@router.put("/notes/{note_id}/", response_model=schemas.Note)
def update_note(note_id: int, note: schemas.NoteUpdate, db: Session = Depends(get_db)):
    note = crud.update_note(db=db, note_id=note_id, note=note)

    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")

    return note


@router.delete("/notes/{note_id}/")
def delete_note(note_id: int, db: Session = Depends(get_db)):
    note = crud.get_note(db=db, note_id=note_id)
    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")

    return crud.delete_note(note_id=note_id, db=db)


@router.post("/notes/summarize/{note_id}")
def summarize_note(note_id: int, db: Session = Depends(get_db)):
    note = db.query(models.Note).filter(models.Note.id == note_id).first()
    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")

    summary = summarize_note_with_gemini(note.content)
    return {"note_id": note_id, "summary": summary}


@router.get("/analytics/")
def get_notes_analytics(db: Session = Depends(get_db)):
    notes = crud.get_all_notes(db=db)

    if not notes:
        raise HTTPException(status_code=404, detail="Notes not found")

    return analyze_notes(notes)
