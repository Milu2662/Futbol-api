# Futbol-api
API REST para gestión de cuadrangular de fútbol - FastAPI + PostgreSQL + Docker

# Cuadrangular Fútbol API
[![CI](https://github.com/Milu2662/Futbol-api/actions/workflows/ci.yml/badge.svg)](https://github.com/Milu2662/Futbol-api/actions/workflows/ci.yml)

API REST desarrollada con FastAPI para la gestión de un cuadrangular de fútbol. Permite registrar hasta cuatro equipos, generar automáticamente el fixture de todos contra todos, registrar y consultar marcadores, y calcular en tiempo real la tabla de posiciones según las reglas oficiales del fútbol.

El proyecto incluye una interfaz web funcional para interactuar con la API, persistencia en PostgreSQL, migraciones versionadas con Alembic, suite de pruebas automatizadas y un pipeline de integración continua.

## Tabla de contenidos
- [Stack tecnológico](#stack-tecnológico)
- [Características](#características)
- [Estructura del proyecto](#estructura-del-proyecto)
- [Modelo de datos](#modelo-de-datos)
- [Instrucciones de ejecución](#instrucciones-de-ejecución)
- [Variables de entorno](#variables-de-entorno)
- [Documentación de la API](#documentación-de-la-api)
- [Pruebas automatizadas](#pruebas-automatizadas)
- [Integración y despliegue continuo](#integración-y-despliegue-continuo)
- [Estrategia de ramas](#estrategia-de-ramas)
- [Despliegue](#despliegue)
- [Evidencia de funcionamiento](#evidencia-de-funcionamiento)
- [Autor](#autor)

## Stack tecnológico
| Capa | Tecnología |
|---|---|
| Lenguaje | Python 3.13 |
| Framework API | FastAPI |
| Servidor ASGI | Uvicorn |
| ORM | SQLAlchemy 2.0 |
| Migraciones | Alembic |
| Base de datos | PostgreSQL 16 |
| Validación de datos | Pydantic v2 |
| Pruebas | Pytest, httpx (TestClient) |
| Contenedores | Docker, Docker Compose |
| Integración continua | GitHub Actions |
| Frontend | HTML, CSS y JavaScript, sin frameworks |
| Despliegue | Microsoft Azure (App Service + Azure Database for PostgreSQL) |
| Registro de contenedores | Docker Hub |

## Características
- Registro de hasta cuatro equipos, con la restricción aplicada en la capa de negocio.
- Generación automática del fixture de todos contra todos (seis partidos para cuatro equipos).
- Registro y edición de marcadores por partido.
- Cálculo dinámico de la tabla de posiciones, con criterios de desempate por puntos, diferencia de gol y goles a favor.
- Operaciones CRUD completas sobre equipos, incluyendo eliminación con borrado en cascada de los partidos asociados.
- Endpoint de reinicio del torneo para iniciar un nuevo cuadrangular sin intervención manual sobre la base de datos.
- Autenticación basada en JWT: todos los endpoints de la API requieren un token válido, obtenido mediante un endpoint de inicio de sesión.
- Trazabilidad de creación de equipos: cada equipo registra qué usuario lo creó.
- Interfaz web con pantalla de inicio de sesión y tres vistas: marcadores, tabla de posiciones y administración de equipos.
- Documentación interactiva generada automáticamente mediante OpenAPI/Swagger.
- Suite de veintiún pruebas automatizadas ejecutadas en cada integración.
- Despliegue continuo en la nube sobre un contenedor Docker publicado en Docker Hub.


## Estructura del proyecto
Futbol-api/
├── backend/
│   ├── app/
│   │   ├── api/                  # Endpoints REST
│   │   │   ├── equipos.py
│   │   │   ├── partidos.py
│   │   │   ├── tabla_posiciones.py
│   │   │   └── torneo.py
│   │   ├── core/
│   │   │   └── config.py         # Configuración y variables de entorno
│   │   ├── db/
│   │   │   └── session.py        # Conexión a la base de datos
│   │   ├── models/                # Modelos SQLAlchemy
│   │   │   ├── equipo.py
│   │   │   └── partido.py
│   │   ├── schemas/                # Esquemas Pydantic de entrada y salida
│   │   │   ├── equipo.py
│   │   │   ├── partido.py
│   │   │   └── tabla_posiciones.py
│   │   ├── services/                # Lógica de negocio
│   │   │   ├── equipo_service.py
│   │   │   ├── partido_service.py
│   │   │   ├── tabla_posiciones_service.py
│   │   │   └── torneo_service.py
│   │   └── main.py                   # Punto de entrada de la aplicación
│   ├── alembic/                        # Migraciones de base de datos
│   ├── tests/                           # Pruebas automatizadas
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── css/style.css
│   ├── js/
│   └── index.html
├── frontend/

│   ├── css/style.css

│   ├── js/                             # api.js, auth.js, ui.js, tabs.js, equipos.js, partidos.js, tabla.js, app.js
│   └── index.html
├── docs/
│   ├── diagrama-er.png
│   └── screenshots/
├── .github/workflows/ci.yml
├── docker-compose.yml
├── .env.example
└── README.md

La aplicación está organizada por capas, separando claramente la lógica de negocio de los modelos de datos y de la capa de presentación:

- `models/` define la estructura de las tablas y su persistencia.
- `schemas/` define los contratos de entrada y salida de la API, desacoplados de los modelos de base de datos.
- `services/` concentra las reglas de negocio (límite de equipos, generación de fixture, cálculo de tabla de posiciones).
- `api/` actúa exclusivamente como capa de traducción entre las peticiones HTTP y los servicios.
- `frontend/` consume la API mediante peticiones `fetch` y no contiene lógica de negocio.

## Modelo de datos
![Diagrama entidad-relación](docs/diagrama-er.png)

**Usuario**

| Campo | Tipo | Descripción |
|---|---|---|
| id | Integer (PK) | Identificador único |
| username | String, único | Nombre de usuario para inicio de sesión |
| hashed_password | String | Contraseña hasheada con bcrypt |
| creado_en | DateTime | Fecha de creación |

**Equipo**

| Campo | Tipo | Descripción |
|---|---|---|
| id | Integer (PK) | Identificador único |
| nombre | String, único | Nombre del equipo |
| fecha_creacion | DateTime | Fecha de registro |
| registrado_por_id | Integer (FK → Usuario), opcional | Usuario que registró el equipo |

**Partido**

| Campo | Tipo | Descripción |
|---|---|---|
| id | Integer (PK) | Identificador único |
| equipo_local_id | Integer (FK → Equipo) | Equipo local |
| equipo_visitante_id | Integer (FK → Equipo) | Equipo visitante |
| goles_local | Integer, nullable | Marcador del equipo local |
| goles_visitante | Integer, nullable | Marcador del equipo visitante |
| jugado | Boolean | Indica si el partido tiene marcador registrado |
| fecha_juego | DateTime, nullable | Fecha del encuentro |

La tabla de posiciones no se persiste como entidad independiente: se calcula dinámicamente a partir de los partidos jugados, evitando inconsistencias entre datos almacenados y datos derivados.

Al iniciar la aplicación por primera vez, se crea automáticamente un usuario administrador a partir de las variables de entorno `ADMIN_USERNAME` y `ADMIN_PASSWORD`, evitando la necesidad de un endpoint público de registro.


## Instrucciones de ejecución

### Prerrequisitos

- Docker Desktop (incluye Docker Compose)
- Git

### Clonar el repositorio

```bash
git clone https://github.com/Milu2662/Futbol-api.git
cd Futbol-api
```

### Configurar variables de entorno

```bash
cp .env.example .env
```

En Windows, mediante PowerShell:

```powershell
Copy-Item .env.example .env
```

### Ejecución con Docker (recomendada)

```bash
docker compose up --build
```

Este comando levanta PostgreSQL y el backend, ejecuta las migraciones automáticamente y deja disponible:

- API: `http://localhost:8000`
- Interfaz web: `http://localhost:8000/app/`
- Documentación interactiva: `http://localhost:8000/docs`

Al primer arranque se crea el usuario administrador con las credenciales definidas en `.env` (por defecto, usuario `admin`).

### Ejecución local sin Docker
```bash
docker compose up -d db

cd backend
python -m venv venv

# Windows
.\venv\Scripts\Activate.ps1

# Linux / macOS
source venv/bin/activate

pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload
```

## Variables de entorno
| Variable | Descripción | Ejemplo |
|---|---|---|
| `DATABASE_URL` | Cadena de conexión a PostgreSQL | `postgresql://user:pass@localhost:5433/futbol_db` |
| `POSTGRES_USER` | Usuario de la base de datos (uso local con Docker Compose) | `futbol_user` |
| `POSTGRES_PASSWORD` | Contraseña de la base de datos (uso local con Docker Compose) | `futbol_pass` |
| `POSTGRES_DB` | Nombre de la base de datos (uso local con Docker Compose) | `futbol_db` |
| `SECRET_KEY` | Clave usada para firmar los tokens JWT | cadena aleatoria larga |
| `ALGORITHM` | Algoritmo de firma de los tokens | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Minutos de validez del token de acceso | `60` |
| `ADMIN_USERNAME` | Usuario administrador creado al primer arranque | `admin` |
| `ADMIN_PASSWORD` | Contraseña del usuario administrador inicial | contraseña propia |

Los valores de referencia para desarrollo local se encuentran en `.env.example`.

## Documentación de la API
La documentación interactiva completa, generada automáticamente por FastAPI, está disponible en la ruta `/docs` una vez el servidor está en ejecución. Todos los endpoints, a excepción de `/auth/login`, requieren un token JWT válido enviado en el encabezado `Authorization: Bearer <token>`.

### Autenticación
| Método | Endpoint | Descripción |
|---|---|---|
| POST | `/auth/login` | Autentica un usuario y devuelve un token JWT |

### Equipos
| Método | Endpoint | Descripción |
|---|---|---|
| POST | `/equipos/` | Registra un equipo nuevo, con un máximo de cuatro |
| GET | `/equipos/` | Lista todos los equipos registrados |
| GET | `/equipos/{id}` | Consulta un equipo por su identificador |
| PUT | `/equipos/{id}` | Actualiza el nombre o escudo de un equipo |
| DELETE | `/equipos/{id}` | Elimina un equipo y sus partidos asociados |

### Partidos
| Método | Endpoint | Descripción |
|---|---|---|
| POST | `/partidos/generar-fixture` | Genera los seis partidos del todos contra todos |
| GET | `/partidos/` | Lista todos los partidos |
| GET | `/partidos/{id}` | Consulta un partido por su identificador |
| PUT | `/partidos/{id}/marcador` | Registra o edita el marcador de un partido |

### Tabla de posiciones
| Método | Endpoint | Descripción |
|---|---|---|
| GET | `/tabla-posiciones/` | Calcula y devuelve la tabla de posiciones actual |

### Torneo
| Método | Endpoint | Descripción |
|---|---|---|
| DELETE | `/torneo/reiniciar` | Elimina todos los equipos y partidos registrados |

Todos los endpoints devuelven códigos de estado HTTP semánticos. Las violaciones de reglas de negocio responden con `400`, los recursos inexistentes con `404`, las peticiones sin autenticación o con un token inválido con `401`, y las operaciones de creación o eliminación exitosas con `201` o `204`, según corresponda. Las respuestas de error siguen el formato `{"detail": "mensaje descriptivo"}`.

## Pruebas automatizadas
El proyecto cuenta con veintiún pruebas automatizadas escritas con Pytest, ejecutadas sobre una base de datos SQLite en memoria, aislada de la base de datos de desarrollo.

```bash
cd backend
python -m pytest -v
```

Las pruebas cubren:

- Inicio de sesión exitoso y fallido, y acceso a endpoints protegidos con y sin token válido.
- Operaciones CRUD sobre equipos, incluyendo el límite de cuatro registros, validación de nombres duplicados y eliminación en cascada.
- Generación del fixture, incluyendo validaciones sobre la cantidad de equipos y la imposibilidad de generarlo más de una vez.
- Registro de marcadores, incluyendo el rechazo de valores negativos.
- Cálculo de la tabla de posiciones, validando puntuación por victoria y empate, y el orden de clasificación resultante.

## Integración y despliegue continuo

El proyecto cuenta con dos pipelines independientes definidos en `.github/workflows/`:

**CI (`ci.yml`)**: se ejecuta en cada push a `develop` y en cada Pull Request hacia `main`.
Instala las dependencias, ejecuta la suite de 21 pruebas automatizadas y genera un reporte
de cobertura. Actua como verificacion obligatoria antes de integrar cambios a la rama principal.

**CD (`cd.yml`)**: se ejecuta automaticamente en cada push a `main`. Construye la imagen
Docker de la aplicacion, la publica en Docker Hub, y dispara el redespliegue en Azure App
Service mediante una llamada autenticada al endpoint de despliegue (Kudu), verificando el
codigo de respuesta para que el pipeline falle de forma visible si Azure rechaza la solicitud.

Flujo completo: push a `main` -> CI ya validado en el Pull Request -> CD construye y publica
la imagen -> Azure App Service descarga la imagen nueva y reinicia el contenedor, sin
intervencion manual posterior al merge.

## Estrategia de ramas
main        Versión estable, desplegable a producción
develop     Rama de integración de funcionalidades
feature/*   Una rama por funcionalidad, integrada mediante Pull Request
fix/*       Correcciones puntuales
docs/*      Cambios de documentación

Los mensajes de commit siguen la convención [Conventional Commits](https://www.conventionalcommits.org/) (`feat:`, `fix:`, `docs:`, `test:`, `ci:`, `chore:`), facilitando la trazabilidad del historial de cambios.

## Despliegue

**URL de producción:** https://futbol-api-milu2662.azurewebsites.net

**Interfaz web:** https://futbol-api-milu2662.azurewebsites.net/app/

**Documentación interactiva:** https://futbol-api-milu2662.azurewebsites.net/docs

La aplicación está desplegada sobre Microsoft Azure, utilizando los siguientes recursos:

| Recurso | Servicio de Azure | Detalle |
|---|---|---|
| Backend | App Service (Linux, plan F1) | Ejecuta la imagen Docker publicada en Docker Hub |
| Base de datos | Azure Database for PostgreSQL – Flexible Server | Capa Burstable (B1ms) |
| Imagen de contenedor | Docker Hub | Repositorio público `milu2662/futbol-api` |

El backend y el frontend se sirven desde un único contenedor: el backend expone la API REST y, adicionalmente, sirve los archivos estáticos del frontend en la ruta `/app`. Las migraciones de base de datos se ejecutan automáticamente al iniciar el contenedor.

## Evidencia de funcionamiento
A continuación se muestran capturas de la interfaz funcionando sobre los datos de prueba.

![Inicio de sesión](docs/screenshots/login.png)
![Marcadores](docs/screenshots/marcadores.png)
![Tabla de posiciones](docs/screenshots/tabla.png)
![Administración de equipos](docs/screenshots/equipos.png)

## Autor
[Milu2662](https://github.com/Milu2662)