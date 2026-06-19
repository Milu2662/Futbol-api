from sqlalchemy.orm import Session, joinedload

from app.models.equipo import Equipo
from app.models.partido import Partido
from app.schemas.tabla_posiciones import PosicionEquipo

PUNTOS_GANADOR = 3
PUNTOS_EMPATE = 1
PUNTOS_PERDEDOR = 0


def calcular_tabla_posiciones(db: Session) -> list[PosicionEquipo]:
    equipos = db.query(Equipo).all()
    partidos_jugados = (
        db.query(Partido)
        .filter(Partido.jugado == True)  # noqa: E712
        .options(joinedload(Partido.equipo_local), joinedload(Partido.equipo_visitante))
        .all()
    )

    # Inicializa estadísticas en cero para cada equipo
    estadisticas: dict[int, dict] = {
        equipo.id: {
            "equipo_id": equipo.id,
            "nombre": equipo.nombre,
            "partidos_jugados": 0,
            "ganados": 0,
            "empatados": 0,
            "perdidos": 0,
            "goles_favor": 0,
            "goles_contra": 0,
            "puntos": 0,
        }
        for equipo in equipos
    }

    for partido in partidos_jugados:
        local = estadisticas[partido.equipo_local_id]
        visitante = estadisticas[partido.equipo_visitante_id]

        local["partidos_jugados"] += 1
        visitante["partidos_jugados"] += 1

        local["goles_favor"] += partido.goles_local
        local["goles_contra"] += partido.goles_visitante
        visitante["goles_favor"] += partido.goles_visitante
        visitante["goles_contra"] += partido.goles_local

        if partido.goles_local > partido.goles_visitante:
            local["ganados"] += 1
            local["puntos"] += PUNTOS_GANADOR
            visitante["perdidos"] += 1
            visitante["puntos"] += PUNTOS_PERDEDOR
        elif partido.goles_local < partido.goles_visitante:
            visitante["ganados"] += 1
            visitante["puntos"] += PUNTOS_GANADOR
            local["perdidos"] += 1
            local["puntos"] += PUNTOS_PERDEDOR
        else:
            local["empatados"] += 1
            local["puntos"] += PUNTOS_EMPATE
            visitante["empatados"] += 1
            visitante["puntos"] += PUNTOS_EMPATE

    tabla = [
        PosicionEquipo(
            **stats,
            diferencia_goles=stats["goles_favor"] - stats["goles_contra"],
        )
        for stats in estadisticas.values()
    ]

    # Orden oficial de fútbol: 1° puntos, 2° diferencia de gol, 3° goles a favor
    tabla.sort(
        key=lambda p: (p.puntos, p.diferencia_goles, p.goles_favor),
        reverse=True,
    )

    return tabla