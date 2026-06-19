def _crear_4_equipos(client):
    nombres = ["Equipo A", "Equipo B", "Equipo C", "Equipo D"]
    for nombre in nombres:
        client.post("/equipos/", json={"nombre": nombre})


def test_generar_fixture_crea_6_partidos(client):
    _crear_4_equipos(client)
    response = client.post("/partidos/generar-fixture")
    assert response.status_code == 201
    assert len(response.json()) == 6


def test_no_genera_fixture_sin_4_equipos(client):
    client.post("/equipos/", json={"nombre": "Solo Uno"})
    response = client.post("/partidos/generar-fixture")
    assert response.status_code == 400


def test_no_genera_fixture_dos_veces(client):
    _crear_4_equipos(client)
    client.post("/partidos/generar-fixture")
    response = client.post("/partidos/generar-fixture")
    assert response.status_code == 400


def test_actualizar_marcador(client):
    _crear_4_equipos(client)
    partidos = client.post("/partidos/generar-fixture").json()
    partido_id = partidos[0]["id"]

    response = client.put(
        f"/partidos/{partido_id}/marcador",
        json={"goles_local": 3, "goles_visitante": 1},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["jugado"] is True
    assert data["goles_local"] == 3


def test_rechaza_goles_negativos(client):
    _crear_4_equipos(client)
    partidos = client.post("/partidos/generar-fixture").json()
    partido_id = partidos[0]["id"]

    response = client.put(
        f"/partidos/{partido_id}/marcador",
        json={"goles_local": -1, "goles_visitante": 2},
    )
    assert response.status_code == 400