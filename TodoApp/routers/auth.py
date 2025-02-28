from fastapi import APIRouter

# Normally we import app.get but we can make router to switch it.

router = APIRouter()

@router.get("/auth/")
async def get_user():
    return {}