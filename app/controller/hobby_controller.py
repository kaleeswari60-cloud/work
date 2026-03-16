from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select

from database import SessionLocal
from app.model import model
from app.schema import schemas

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/hobbies", response_model=schemas.Hobby)
def create_hobby(hobby: schemas.HobbyCreate, db: Session = Depends(get_db)):

    stmt = select(model.Hobby).where(model.Hobby.hobby_name == hobby.hobby_name)
    existing = db.execute(stmt).scalar_one_or_none()

    if existing:
        raise HTTPException(status_code=400, detail="Hobby already exists")

    db_hobby = model.Hobby(hobby_name=hobby.hobby_name)

    db.add(db_hobby)
    db.commit()
    db.refresh(db_hobby)

    return db_hobby


@router.get("/hobbies", response_model=list[schemas.Hobby])
def get_hobbies(db: Session = Depends(get_db)):

    stmt = select(model.Hobby)
    hobbies = db.execute(stmt).scalars().all()

    return hobbies