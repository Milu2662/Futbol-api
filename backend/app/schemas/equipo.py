from datetime import datetime
from pydantic import BaseModel, ConfigDict


class EquipoBase(BaseModel):
    nombre: str
    escudo_url: str | None = None


class EquipoCreate(EquipoBase):
    pass


class EquipoUpdate(BaseModel):
    nombre: str | None = None
    escudo_url: str | None = None


class EquipoOut(EquipoBase):
    id: int
    fecha_creacion: datetime
    registrado_por_id: int | None = None

    model_config = ConfigDict(from_attributes=True)