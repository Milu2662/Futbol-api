from sqlalchemy import Column, Integer, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship

from app.db.session import Base


class Partido(Base):
    __tablename__ = "partidos"

    id = Column(Integer, primary_key=True, index=True)

    equipo_local_id = Column(Integer, ForeignKey("equipos.id"), nullable=False)
    equipo_visitante_id = Column(Integer, ForeignKey("equipos.id"), nullable=False)

    goles_local = Column(Integer, nullable=True)
    goles_visitante = Column(Integer, nullable=True)
    jugado = Column(Boolean, default=False, nullable=False)
    fecha_juego = Column(DateTime(timezone=True), nullable=True)

    equipo_local = relationship(
        "Equipo",
        foreign_keys=[equipo_local_id],
        back_populates="partidos_local",
    )
    equipo_visitante = relationship(
        "Equipo",
        foreign_keys=[equipo_visitante_id],
        back_populates="partidos_visitante",
    )