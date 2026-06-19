from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.tabla_posiciones import PosicionEquipo
from app.services import tabla_posiciones_service

router = APIRouter(prefix="/tabla-posiciones", tags=["Tabla de posiciones"])


@router.get("/", response_model=list[PosicionEquipo])
def obtener_tabla_posiciones(db: Session = Depends(get_db)):
    return tabla_posiciones_service.calcular_tabla_posiciones(db)
