from datetime import datetime, timedelta, timezone

import bcrypt
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.session import get_db
from app.models.usuario import Usuario

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verificar_password(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))


def crear_access_token(username: str) -> str:
    expira = datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_expire_minutes)
    payload = {"sub": username, "exp": expira}
    return jwt.encode(payload, settings.secret_key, algorithm=settings.algorithm)


def autenticar_usuario(db: Session, username: str, password: str) -> Usuario | None:
    usuario = db.query(Usuario).filter(Usuario.username == username).first()
    if not usuario:
        return None
    if not verificar_password(password, usuario.hashed_password):
        return None
    return usuario


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> Usuario:
    credenciales_invalidas = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudo validar las credenciales.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        username = payload.get("sub")
        if username is None:
            raise credenciales_invalidas
    except jwt.PyJWTError:
        raise credenciales_invalidas

    usuario = db.query(Usuario).filter(Usuario.username == username).first()
    if usuario is None:
        raise credenciales_invalidas
    return usuario


def seed_admin_user(db: Session) -> None:
    """Crea el usuario administrador inicial si todavía no existe ningún usuario."""
    existe_alguno = db.query(Usuario).first()
    if existe_alguno:
        return

    admin = Usuario(
        username=settings.admin_username,
        hashed_password=hash_password(settings.admin_password),
    )
    db.add(admin)
    db.commit()