from typing import List

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
import uvicorn

from database import (
    Base,
    engine,
    SessionLocal
)

from models import (
    Note,
    Checklist,
    Address
)

from schemas import (
    NoteCreate,
    ChecklistCreate
)

Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()

@app.post("/notes/sync")
def create_note(
    notes_data: List[NoteCreate],
    db: Session = Depends(get_db)
):

    notes = []

    for note_data in notes_data:
        address = None

        if note_data.address:

            address = Address(
                latitude=note_data.address.latitude,
                longitude=note_data.address.longitude
            )

            db.add(address)
            db.flush()

        note = Note(
            title=note_data.title,
            content=note_data.content,
            timestamp=note_data.timestamp,
            priority=note_data.priority,
            address_id=address.id if address else None
        )

        db.add(note)
        notes.append(note)

    db.commit()

    for note in notes:
        db.refresh(note)

    return {
        "message": "Notes created",
        "ids": [note.id for note in notes]
    }

@app.post("/checklists/sync")
def create_checklist(
    checklists_data: List[ChecklistCreate],
    db: Session = Depends(get_db)
):

    checklists = []

    for checklist_data in checklists_data:
        checklist = Checklist(
            title=checklist_data.title,
            is_completed=checklist_data.isCompleted,
            priority=checklist_data.priority
        )

        db.add(checklist)
        checklists.append(checklist)

    db.commit()

    for checklist in checklists:
        db.refresh(checklist)

    return {
        "message": "Checklists created",
        "ids": [checklist.id for checklist in checklists]
    }

if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=666)