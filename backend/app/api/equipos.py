from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.usuario import Usuario
from app.schemas.equipo import EquipoCreate, EquipoUpdate, EquipoOut
from app.services import equipo_service
from app.services.auth_service import get_current_user

router = APIRouter(prefix="/equipos", tags=["Equipos"])


@router.post("/", response_model=EquipoOut, status_code=status.HTTP_201_CREATED)
def crear_equipo(
    equipo: EquipoCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    return equipo_service.crear_equipo(db, equipo, current_user)


@router.get("/", response_model=list[EquipoOut])
def listar_equipos(db: Session = Depends(get_db)):
    return equipo_service.obtener_equipos(db)


@router.get("/{equipo_id}", response_model=EquipoOut)
def obtener_equipo(equipo_id: int, db: Session = Depends(get_db)):
    return equipo_service.obtener_equipo_por_id(db, equipo_id)


@router.put("/{equipo_id}", response_model=EquipoOut)
def actualizar_equipo(equipo_id: int, equipo: EquipoUpdate, db: Session = Depends(get_db)):
    return equipo_service.actualizar_equipo(db, equipo_id, equipo)


@router.delete("/{equipo_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_equipo(equipo_id: int, db: Session = Depends(get_db)):
    equipo_service.eliminar_equipo(db, equipo_id)