const API_BASE = '';

async function apiRequest(path, options = {}) {
  const res = await fetch(`${API_BASE}${path}`, {
    headers: { 'Content-Type': 'application/json' },
    ...options,
  });
  if (res.status === 204) return null;
  const data = await res.json().catch(() => ({}));
  if (!res.ok) {
    throw new Error(data.detail || 'Ocurrió un error inesperado.');
  }
  return data;
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