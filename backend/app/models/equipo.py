from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.session import Base


class Equipo(Base):
    __tablename__ = "equipos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), unique=True, nullable=False)
    escudo_url = Column(String(255), nullable=True)
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())
    registrado_por_id = Column(Integer, ForeignKey("usuarios.id"), nullable=True)

    registrado_por = relationship("Usuario")

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