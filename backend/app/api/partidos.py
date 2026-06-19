from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.partido import PartidoUpdateMarcador, PartidoOut
from app.services import partido_service

router = APIRouter(prefix="/partidos", tags=["Partidos"])


@router.post("/generar-fixture", response_model=list[PartidoOut], status_code=status.HTTP_201_CREATED)
def generar_fixture(db: Session = Depends(get_db)):
    return partido_service.generar_fixture(db)


@router.get("/", response_model=list[PartidoOut])
def listar_partidos(db: Session = Depends(get_db)):
    return partido_service.obtener_partidos(db)


@router.get("/{partido_id}", response_model=PartidoOut)
def obtener_partido(partido_id: int, db: Session = Depends(get_db)):
    return partido_service.obtener_partido_por_id(db, partido_id)


@router.put("/{partido_id}/marcador", response_model=PartidoOut)
def actualizar_marcador(partido_id: int, marcador: PartidoUpdateMarcador, db: Session = Depends(get_db)):
    return partido_service.actualizar_marcador(db, partido_id, marcador)