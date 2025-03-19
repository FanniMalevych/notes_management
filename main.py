from fastapi import FastAPI, HTTPException
from fastapi.params import Depends
from sqlalchemy.orm import Session

import crud
import schemas
from analytics import analyze_notes
from db import models
from db.engine import SessionLocal
from ai_summarize import summarize_note_with_gemini

app = FastAPI()


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/notes/", response_model=list[schemas.Note])
def read_notes(db: Session = Depends(get_db)):
    return crud.get_all_notes(db)


@app.get("/notes/{note_id}/", response_model=schemas.Note)
def read_single_note(note_id: int, db: Session = Depends(get_db)):
    note = crud.get_note(db=db, note_id=note_id)

    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")

    return note


@app.post("/notes/", response_model=schemas.Note)
def create_note(note: schemas.NoteCreate, db: Session = Depends(get_db)):
    return crud.create_note(db=db, note=note)


@app.put("/notes/{note_id}/", response_model=schemas.Note)
def update_note(note_id: int, note: schemas.NoteUpdate, db: Session = Depends(get_db)):
    note = crud.update_note(db=db, note_id=note_id, note=note)

    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")

    return note


@app.delete("/notes/{note_id}/")
def delete_note(note_id: int, db: Session = Depends(get_db)):
    note = crud.get_note(db=db, note_id=note_id)
    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")

    return crud.delete_note(note_id=note_id, db=db)


@app.post("/notes/summarize/{note_id}")
def summarize_note(note_id: int, db: Session = Depends(get_db)):
    note = db.query(models.Note).filter(models.Note.id == note_id).first()
    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")

    summary = summarize_note_with_gemini(note.content)
    return {"note_id": note_id, "summary": summary}

@app.get("/analytics/")
def get_notes_analytics(db: Session = Depends(get_db)):
    notes = crud.get_all_notes(db=db)

    if not notes:
        raise HTTPException(status_code=404, detail="Notes not found")

    return analyze_notes(notes)
