from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status

from app.models.equipo import Equipo
from app.schemas.equipo import EquipoCreate, EquipoUpdate

MAX_EQUIPOS = 4


def crear_equipo(db: Session, equipo_data: EquipoCreate) -> Equipo:
    total_equipos = db.query(Equipo).count()
    if total_equipos >= MAX_EQUIPOS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Ya existen {MAX_EQUIPOS} equipos registrados. No se permiten más para el cuadrangular.",
        )

    nuevo_equipo = Equipo(**equipo_data.model_dump())
    db.add(nuevo_equipo)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Ya existe un equipo con el nombre '{equipo_data.nombre}'.",
        )
    db.refresh(nuevo_equipo)
    return nuevo_equipo


def obtener_equipos(db: Session) -> list[Equipo]:
    return db.query(Equipo).all()


def obtener_equipo_por_id(db: Session, equipo_id: int) -> Equipo:
    equipo = db.query(Equipo).filter(Equipo.id == equipo_id).first()
    if not equipo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Equipo con id {equipo_id} no encontrado.",
        )
    return equipo


def actualizar_equipo(db: Session, equipo_id: int, equipo_data: EquipoUpdate) -> Equipo:
    equipo = obtener_equipo_por_id(db, equipo_id)

    datos_actualizados = equipo_data.model_dump(exclude_unset=True)
    for campo, valor in datos_actualizados.items():
        setattr(equipo, campo, valor)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ya existe un equipo con ese nombre.",
        )
    db.refresh(equipo)
    return equipo