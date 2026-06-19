from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.services import torneo_service

router = APIRouter(prefix="/torneo", tags=["Torneo"])


@router.delete("/reiniciar", status_code=status.HTTP_204_NO_CONTENT)
def reiniciar_torneo(db: Session = Depends(get_db)):
    torneo_service.reiniciar_torneo(db)