const API_BASE = '';
const TOKEN_KEY = 'futbol_token';

function getToken() {
  return localStorage.getItem(TOKEN_KEY);
}

function setToken(token) {
  localStorage.setItem(TOKEN_KEY, token);
}

function clearToken() {
  localStorage.removeItem(TOKEN_KEY);
}

async function apiRequest(path, options = {}) {
  const headers = { 'Content-Type': 'application/json', ...options.headers };
  const token = getToken();
  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }

  const res = await fetch(`${API_BASE}${path}`, { ...options, headers });

  if (res.status === 401) {
    clearToken();
    mostrarLogin();
    throw new Error('Sesión expirada. Vuelve a iniciar sesión.');
  }

  if (res.status === 204) return null;

  const data = await res.json().catch(() => ({}));
  if (!res.ok) {
    throw new Error(data.detail || 'Ocurrió un error inesperado.');
  }
  return data;
}

async function login(username, password) {
  const body = new URLSearchParams();
  body.append('username', username);
  body.append('password', password);

  const res = await fetch(`${API_BASE}/auth/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body,
  });

  const data = await res.json().catch(() => ({}));
  if (!res.ok) {
    throw new Error(data.detail || 'Usuario o contraseña incorrectos.');
  }

  setToken(data.access_token);
}

const api = {
  getEquipos: () => apiRequest('/equipos/'),
  crearEquipo: (nombre) => apiRequest('/equipos/', { method: 'POST', body: JSON.stringify({ nombre }) }),
  actualizarEquipo: (id, nombre) => apiRequest(`/equipos/${id}`, { method: 'PUT', body: JSON.stringify({ nombre }) }),
  eliminarEquipo: (id) => apiRequest(`/equipos/${id}`, { method: 'DELETE' }),
  getPartidos: () => apiRequest('/partidos/'),
  generarFixture: () => apiRequest('/partidos/generar-fixture', { method: 'POST' }),
  actualizarMarcador: (id, golesLocal, golesVisitante) =>
    apiRequest(`/partidos/${id}/marcador`, {
      method: 'PUT',
      body: JSON.stringify({ goles_local: golesLocal, goles_visitante: golesVisitante }),
    }),
  getTabla: () => apiRequest('/tabla-posiciones/'),
  reiniciarTorneo: () => apiRequest('/torneo/reiniciar', { method: 'DELETE' }),
};