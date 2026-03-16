from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from database import SessionLocal, engine, Base
import models, schemas

Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ---------------- HOBBIES ----------------

@app.post("/hobbies", response_model=schemas.Hobby)
def create_hobby(hobby: schemas.HobbyCreate, db: Session = Depends(get_db)):

    stmt = select(models.Hobby).where(models.Hobby.hobby_name == hobby.hobby_name)
    existing = db.execute(stmt).scalar_one_or_none()

    if existing:
        raise HTTPException(status_code=400, detail="Hobby already exists")

    db_hobby = models.Hobby(hobby_name=hobby.hobby_name)

    db.add(db_hobby)
    db.commit()
    db.refresh(db_hobby)

    return db_hobby


@app.get("/hobbies", response_model=list[schemas.Hobby])
def get_hobbies(db: Session = Depends(get_db)):

    stmt = select(models.Hobby)
    hobbies = db.execute(stmt).scalars().all()

    return hobbies


# ---------------- USERS ----------------

@app.post("/users", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    stmt = select(models.User).where(models.User.email == user.email)
    existing_email = db.execute(stmt).scalar_one_or_none()

    if existing_email:
        raise HTTPException(status_code=400, detail="Email already registered")

    db_user = models.User(
        first_name=user.first_name,
        last_name=user.last_name,
        date_of_birth=user.date_of_birth,
        email=user.email,
        password=user.password,
        country=user.country,
        city=user.city
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    for hobby_id in user.hobbies:
        relation = models.UserHobby(
            user_id=db_user.id,
            hobby_id=hobby_id
        )
        db.add(relation)

    db.commit()

    return db_user


@app.get("/users", response_model=list[schemas.User])
def get_users(db: Session = Depends(get_db)):

    stmt = select(models.User)
    users = db.execute(stmt).scalars().all()

    return users


# ---------------- USER HOBBIES ----------------

@app.get("/users/by-hobby/{hobby_id}", response_model=list[schemas.User])
def get_users_by_hobby(hobby_id: int, db: Session = Depends(get_db)):

    stmt = (
        select(models.User)
        .join(models.UserHobby, models.User.id == models.UserHobby.user_id)
        .where(models.UserHobby.hobby_id == hobby_id)
    )

    users = db.execute(stmt).scalars().all()

    if not users:
        raise HTTPException(
            status_code=404,
            detail="No users found with this hobby id"
        )

    return users