from fastapi import FastAPI, HTTPException
from fastapi.params import Depends
from sqlalchemy.orm import Session

import crud
import schemas
from db.engine import SessionLocal

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
    db_note = crud.get_note(db=db, note_id=note_id)

    if db_note is None:
        raise HTTPException(status_code=404, detail="Note not found")

    return db_note


@app.post("/notes/", response_model=schemas.Note)
def create_note(note: schemas.NoteCreate, db: Session = Depends(get_db)):
    return crud.create_note(db=db, note=note)


@app.put("/notes/{note_id}/", response_model=schemas.Note)
def update_note(note_id: int, note: schemas.NoteUpdate, db: Session = Depends(get_db)):
    db_note = crud.update_note(db=db, note_id=note_id, note=note)

    if db_note is None:
        raise HTTPException(status_code=404, detail="Note not found")

    return db_note


@app.delete("/notes/{note_id}/")
def delete_note(note_id: int, db: Session = Depends(get_db)):
    return crud.delete_note(note_id=note_id, db=db)
