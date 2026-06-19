from datetime import datetime
from pydantic import BaseModel, ConfigDict

from app.schemas.equipo import EquipoOut


class PartidoBase(BaseModel):
    equipo_local_id: int
    equipo_visitante_id: int
    fecha_juego: datetime | None = None


class PartidoCreate(PartidoBase):
    """Para crear un partido manualmente (sin marcador aún)"""
    pass


class PartidoUpdateMarcador(BaseModel):
    """Para registrar/editar el marcador de un partido existente"""
    goles_local: int
    goles_visitante: int


class PartidoOut(BaseModel):
    id: int
    goles_local: int | None
    goles_visitante: int | None
    jugado: bool
    fecha_juego: datetime | None
    equipo_local: EquipoOut
    equipo_visitante: EquipoOut

    model_config = ConfigDict(from_attributes=True)
