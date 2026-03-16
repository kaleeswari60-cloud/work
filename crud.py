from sqlalchemy.orm import Session
import models


def create_user(db: Session, user, hobby_ids):

    hobbies = db.query(models.Hobby).filter(models.Hobby.id.in_(hobby_ids)).all()

    db_user = models.User(
        first_name=user.first_name,
        last_name=user.last_name,
        date_of_birth=user.date_of_birth,
        email=user.email,
        password=user.password,
        country=user.country,
        city=user.city,
        hobbies=hobbies
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


def get_users(db: Session):
    return db.query(models.User).all()


def get_users_by_hobby(db: Session, hobby_id: int):
    return (
        db.query(models.User)
        .join(models.User.hobbies)
        .filter(models.Hobby.id == hobby_id)
        .all()
    )