from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import equipos, partidos

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


@app.get("/", tags=["Root"])
def root():
    return {"mensaje": "Cuadrangular Fútbol API - usa /docs para ver la documentación interactiva"}