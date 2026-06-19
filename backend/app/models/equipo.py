from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.session import Base


class Equipo(Base):
    __tablename__ = "equipos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), unique=True, nullable=False)
    escudo_url = Column(String(255), nullable=True)
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())

    # Relaciones inversas: permiten hacer equipo.partidos_local, equipo.partidos_visitante
    partidos_local = relationship(
        "Partido",
        foreign_keys="Partido.equipo_local_id",
        back_populates="equipo_local",
    )
    partidos_visitante = relationship(
        "Partido",
        foreign_keys="Partido.equipo_visitante_id",
        back_populates="equipo_visitante",
    )