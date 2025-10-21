from fastapi import APIRouter
from controllers.status_controller import get_status

router = APIRouter()

@router.get("/status")
def status():
    return get_status()
