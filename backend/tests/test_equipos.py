def test_crear_equipo(client):
    response = client.post("/equipos/", json={"nombre": "Real Madrid", "escudo_url": None})
    assert response.status_code == 201
    data = response.json()
    assert data["nombre"] == "Real Madrid"
    assert "id" in data


def test_no_permite_mas_de_4_equipos(client):
    nombres = ["Equipo A", "Equipo B", "Equipo C", "Equipo D"]
    for nombre in nombres:
        response = client.post("/equipos/", json={"nombre": nombre})
        assert response.status_code == 201

    response = client.post("/equipos/", json={"nombre": "Equipo E"})
    assert response.status_code == 400
    assert "4 equipos" in response.json()["detail"]


def test_no_permite_nombres_duplicados(client):
    client.post("/equipos/", json={"nombre": "Barcelona"})
    response = client.post("/equipos/", json={"nombre": "Barcelona"})
    assert response.status_code == 400


def test_listar_equipos_vacio(client):
    response = client.get("/equipos/")
    assert response.status_code == 200
    assert response.json() == []


def test_obtener_equipo_inexistente(client):
    response = client.get("/equipos/999")
    assert response.status_code == 404


def test_actualizar_equipo(client):
    crear = client.post("/equipos/", json={"nombre": "Boca Juniors"})
    equipo_id = crear.json()["id"]

    response = client.put(f"/equipos/{equipo_id}", json={"nombre": "Boca Juniors FC"})
    assert response.status_code == 200
    assert response.json()["nombre"] == "Boca Juniors FC"