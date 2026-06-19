def _crear_y_jugar_fixture(client):
    nombres = ["Equipo A", "Equipo B", "Equipo C", "Equipo D"]
    for nombre in nombres:
        client.post("/equipos/", json={"nombre": nombre})

    partidos = client.post("/partidos/generar-fixture").json()
    return partidos


def test_tabla_vacia_si_no_hay_partidos_jugados(client):
    _crear_y_jugar_fixture(client)
    response = client.get("/tabla-posiciones/")
    assert response.status_code == 200
    tabla = response.json()
    assert len(tabla) == 4
    assert all(equipo["puntos"] == 0 for equipo in tabla)


def test_calculo_de_puntos_por_victoria(client):
    partidos = _crear_y_jugar_fixture(client)
    primer_partido = partidos[0]

    client.put(
        f"/partidos/{primer_partido['id']}/marcador",
        json={"goles_local": 2, "goles_visitante": 0},
    )

    tabla = client.get("/tabla-posiciones/").json()
    ganador_id = primer_partido["equipo_local"]["id"]
    perdedor_id = primer_partido["equipo_visitante"]["id"]

    ganador = next(e for e in tabla if e["equipo_id"] == ganador_id)
    perdedor = next(e for e in tabla if e["equipo_id"] == perdedor_id)

    assert ganador["puntos"] == 3
    assert ganador["ganados"] == 1
    assert perdedor["puntos"] == 0
    assert perdedor["perdidos"] == 1


def test_calculo_de_puntos_por_empate(client):
    partidos = _crear_y_jugar_fixture(client)
    primer_partido = partidos[0]

    client.put(
        f"/partidos/{primer_partido['id']}/marcador",
        json={"goles_local": 1, "goles_visitante": 1},
    )

    tabla = client.get("/tabla-posiciones/").json()
    for equipo in tabla:
        if equipo["equipo_id"] in (
            primer_partido["equipo_local"]["id"],
            primer_partido["equipo_visitante"]["id"],
        ):
            assert equipo["puntos"] == 1
            assert equipo["empatados"] == 1


def test_orden_de_tabla_por_puntos(client):
    partidos = _crear_y_jugar_fixture(client)

    # Hacemos que el primer equipo gane todos sus partidos
    equipo_a_id = partidos[0]["equipo_local"]["id"]
    for partido in partidos:
        if partido["equipo_local"]["id"] == equipo_a_id:
            client.put(
                f"/partidos/{partido['id']}/marcador",
                json={"goles_local": 5, "goles_visitante": 0},
            )
        elif partido["equipo_visitante"]["id"] == equipo_a_id:
            client.put(
                f"/partidos/{partido['id']}/marcador",
                json={"goles_local": 0, "goles_visitante": 5},
            )

    tabla = client.get("/tabla-posiciones/").json()
    assert tabla[0]["equipo_id"] == equipo_a_id
    assert tabla[0]["puntos"] == 9  