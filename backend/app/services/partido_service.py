from itertools import combinations
from sqlalchemy.orm import Session, joinedload
from fastapi import HTTPException, status

from app.models.equipo import Equipo
from app.models.partido import Partido
from app.schemas.partido import PartidoUpdateMarcador


def generar_fixture(db: Session) -> list[Partido]:
    """
    Genera automáticamente todos los partidos del todos-contra-todos
    (round-robin) a partir de los equipos registrados.
    """
    equipos = db.query(Equipo).all()

    if len(equipos) != 4:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Se necesitan exactamente 4 equipos para generar el fixture. Hay {len(equipos)} registrados.",
        )

    partidos_existentes = db.query(Partido).count()
    if partidos_existentes > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El fixture ya fue generado anteriormente. No se puede generar dos veces.",
        )

    nuevos_partidos = []
    # combinations genera todas las parejas únicas: (A,B) (A,C) (A,D) (B,C) (B,D) (C,D)
    for equipo_local, equipo_visitante in combinations(equipos, 2):
        partido = Partido(
            equipo_local_id=equipo_local.id,
            equipo_visitante_id=equipo_visitante.id,
            jugado=False,
        )
        db.add(partido)
        nuevos_partidos.append(partido)

    db.commit()
    for p in nuevos_partidos:
        db.refresh(p)

    return nuevos_partidos


def obtener_partidos(db: Session) -> list[Partido]:
    return (
        db.query(Partido)
        .options(joinedload(Partido.equipo_local), joinedload(Partido.equipo_visitante))
        .all()
    )


def obtener_partido_por_id(db: Session, partido_id: int) -> Partido:
    partido = (
        db.query(Partido)
        .options(joinedload(Partido.equipo_local), joinedload(Partido.equipo_visitante))
        .filter(Partido.id == partido_id)
        .first()
    )
    if not partido:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Partido con id {partido_id} no encontrado.",
        )
    return partido


def actualizar_marcador(db: Session, partido_id: int, marcador: PartidoUpdateMarcador) -> Partido:
    partido = obtener_partido_por_id(db, partido_id)

    if marcador.goles_local < 0 or marcador.goles_visitante < 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Los goles no pueden ser negativos.",
        )

    partido.goles_local = marcador.goles_local
    partido.goles_visitante = marcador.goles_visitante
    partido.jugado = True

    db.commit()
    db.refresh(partido)
    return partido