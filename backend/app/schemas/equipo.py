from datetime import datetime
from pydantic import BaseModel, ConfigDict


class EquipoBase(BaseModel):
    nombre: str
    escudo_url: str | None = None


class EquipoCreate(EquipoBase):
    """Datos requeridos para crear un equipo (POST)"""
    pass


class EquipoUpdate(BaseModel):
    """Datos opcionales para actualizar un equipo (PUT/PATCH) - todo opcional"""
    nombre: str | None = None
    escudo_url: str | None = None


class EquipoOut(EquipoBase):
    """Lo que la API devuelve al cliente"""
    id: int
    fecha_creacion: datetime

    model_config = ConfigDict(from_attributes=True)