from fastapi import APIRouter
from app.controller import user_controller, hobby_controller

router = APIRouter()

router.include_router(user_controller.router, tags=["Users"])
router.include_router(hobby_controller.router, tags=["Hobbies"])