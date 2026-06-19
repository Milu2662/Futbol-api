import os
from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.api import equipos, partidos, tabla_posiciones, torneo, auth
from app.db.session import SessionLocal
from app.services.auth_service import seed_admin_user, get_current_user


@asynccontextmanager
async def lifespan(app: FastAPI):
    db = SessionLocal()
    try:
        seed_admin_user(db)
    finally:
        db.close()
    yield


app = FastAPI(
    title="Cuadrangular Fútbol API",
    description="API REST para gestionar un cuadrangular de fútbol: equipos, partidos y tabla de posiciones.",
    version="1.0.1",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(equipos.router, dependencies=[Depends(get_current_user)])
app.include_router(partidos.router, dependencies=[Depends(get_current_user)])
app.include_router(tabla_posiciones.router, dependencies=[Depends(get_current_user)])
app.include_router(torneo.router, dependencies=[Depends(get_current_user)])

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")
app.mount("/app", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")


@app.get("/", tags=["Root"])
def root():
    return {
        "mensaje": "Cuadrangular Fútbol API",
        "documentacion": "/docs",
        "interfaz_web": "/app",
    }