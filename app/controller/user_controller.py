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


@router.post("/users", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    stmt = select(model.User).where(model.User.email == user.email)
    existing_email = db.execute(stmt).scalar_one_or_none()

    if existing_email:
        raise HTTPException(status_code=400, detail="Email already registered")

    db_user = model.User(
        first_name=user.first_name,
        last_name=user.last_name,
        date_of_birth=user.date_of_birth,
        email=user.email,
        password=user.password,
        country=user.country,
        city=user.city
    )

    hobbies = db.query(model.Hobby).filter(model.Hobby.id.in_(user.hobbies)).all()

    db_user.hobbies = hobbies

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


@router.get("/users", response_model=list[schemas.User])
def get_users(db: Session = Depends(get_db)):

    stmt = select(model.User)
    users = db.execute(stmt).scalars().all()

    return users


@router.get("/users/by-hobby/{hobby_id}", response_model=list[schemas.User])
def get_users_by_hobby(hobby_id: int, db: Session = Depends(get_db)):

    stmt = (
        select(model.User)
        .join(model.user_hobbies)
        .where(model.user_hobbies.c.hobby_id == hobby_id)
    )

    users = db.execute(stmt).scalars().all()

    if not users:
        raise HTTPException(status_code=404, detail="No users found")

    return users