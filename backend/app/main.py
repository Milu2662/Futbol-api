import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.api import equipos, partidos, tabla_posiciones, torneo

app = FastAPI(
    title="Cuadrangular Fútbol API",
    description="API REST para gestionar un cuadrangular de fútbol: equipos, partidos y tabla de posiciones.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(equipos.router)
app.include_router(partidos.router)
app.include_router(tabla_posiciones.router)
app.include_router(torneo.router)

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