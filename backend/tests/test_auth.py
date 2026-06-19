from app.services.auth_service import hash_password
from app.models.usuario import Usuario


def _crear_usuario_prueba(db_session, username="tester", password="clave123"):
    usuario = Usuario(username=username, hashed_password=hash_password(password))
    db_session.add(usuario)
    db_session.commit()
    return usuario


def test_login_exitoso(client_sin_auth, db_session):
    _crear_usuario_prueba(db_session)

    response = client_sin_auth.post(
        "/auth/login",
        data={"username": "tester", "password": "clave123"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_password_incorrecta(client_sin_auth, db_session):
    _crear_usuario_prueba(db_session)

    response = client_sin_auth.post(
        "/auth/login",
        data={"username": "tester", "password": "incorrecta"},
    )
    assert response.status_code == 401


def test_endpoint_protegido_sin_token(client_sin_auth):
    response = client_sin_auth.get("/equipos/")
    assert response.status_code == 401


def test_endpoint_protegido_con_token(client_sin_auth, db_session):
    _crear_usuario_prueba(db_session)
    login = client_sin_auth.post(
        "/auth/login",
        data={"username": "tester", "password": "clave123"},
    )
    token = login.json()["access_token"]

    response = client_sin_auth.get(
        "/equipos/",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200