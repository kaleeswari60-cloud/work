from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
import modl  
from depend import get_db, engine

app = FastAPI()
modl.Base.metadata.create_all(bind=engine)

@app.get("/insert-data")
def insert_data(db: Session = Depends(get_db)):
    hobbies_map = {
        "Ravi": ["Cricket", "Chess","Dance"],
        "Arun": ["Cricket", "Reading","Music"],
        "Priya": ["Music", "Dance","Cricket"]
    }

    for user_name, hobby_list in hobbies_map.items():
  
        new_user = modl.User(name=user_name)
        db.add(new_user)
        db.flush()  
        for h_name in hobby_list:
            new_hobby = modl.Hobby(name=h_name, user_id=new_user.id)
            db.add(new_hobby)

    db.commit()
    return {"message": "Data inserted successfully!"}

@app.get("/users-by-hobby-name/{hobby_name}")
def get_users_by_name(hobby_name: str, db: Session = Depends(get_db)):
    stmt = (
        select(modl.User.name)
        .join(modl.Hobby)
        .where(modl.Hobby.name.ilike(hobby_name))
    )
    
    result = db.execute(stmt).scalars().all()
    
    if not result:
        raise HTTPException(status_code=404, detail=f"No users found for: {hobby_name}")
        
    print(f"Users with hobby {hobby_name}: {result}") 
    return {"hobby": hobby_name, "users": result}



@app.get("/find-shared-hobbies/{user_id}")
def find_shared_hobbies(user_id: int, db: Session = Depends(get_db)):
    user_hobbies_stmt = select(modl.Hobby.name).where(modl.Hobby.user_id == user_id)
    user_hobbies = db.execute(user_hobbies_stmt).scalars().all()

    if not user_hobbies:
        raise HTTPException(status_code=404, detail="User not found or has no hobbies")

    stmt = (
        select(modl.User.name, modl.Hobby.name)
        .join(modl.Hobby)
        .where(modl.Hobby.name.in_(user_hobbies)) 
        .where(modl.User.id != user_id)           
    )
    
    results = db.execute(stmt).all()

    if not results:
        return {"message": "No other users share these hobbies."}
    shared_list = []
    for row in results:
        shared_list.append({
            "other_user_name": row[0], 
            "shared_hobby": row[1]
        })

    return {
        "target_user_id": user_id,
        "shared_with": shared_list
    }
