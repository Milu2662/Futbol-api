from sqlalchemy.orm import Session

from app.models.partido import Partido
from app.models.equipo import Equipo


def reiniciar_torneo(db: Session) -> None:
    """
    Borra todos los partidos y equipos para empezar un cuadrangular nuevo.
    Se borran los partidos primero por la relación de llave foránea con equipos.
    """
    db.query(Partido).delete()
    db.query(Equipo).delete()
    db.commit()