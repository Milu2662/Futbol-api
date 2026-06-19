import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient

from app.main import app
from app.db.session import Base, get_db
from app.models.usuario import Usuario
from app.services.auth_service import get_current_user

SQLALCHEMY_TEST_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_TEST_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db_session():
    """Crea tablas limpias antes de cada test, las destruye después."""
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db_session):
    """
    Cliente de pruebas con autenticación simulada: evita repetir login
    en cada test de CRUD, ya que eso no es lo que se está probando ahí.
    """

    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    def override_get_current_user():
        return Usuario(id=1, username="test_user", hashed_password="no-aplica")

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_current_user] = override_get_current_user
    yield TestClient(app)
    app.dependency_overrides.clear()


@pytest.fixture(scope="function")
def client_sin_auth(db_session):
    """
    Cliente de pruebas SIN simular autenticación, usado únicamente
    en test_auth.py para probar el flujo real de login.
    """

    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()