from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from sqlalchemy import select
from depend import engine, get_db
import tab

tab.Base.metadata.create_all(bind=engine)
app = FastAPI()
@app.post("/add-employee")
def add_employee(name: str, email: str, phone: str, address: str, db: Session = Depends(get_db)):
    new_emp = tab.Employee(name=name, email=email, phone=phone, address=address)
    db.add(new_emp)
    db.commit()
    db.refresh(new_emp)
    return {"message": "Employee added!", "id": new_emp.id}

@app.get("/get-employees")
def get_employees(db: Session = Depends(get_db)):
    employees = db.scalars(select(tab.Employee)).all()
    return employees
