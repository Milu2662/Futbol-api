from pydantic import BaseModel


class PosicionEquipo(BaseModel):
    equipo_id: int
    nombre: str
    partidos_jugados: int
    ganados: int
    empatados: int
    perdidos: int
    goles_favor: int
    goles_contra: int
    diferencia_goles: int
    puntos: int