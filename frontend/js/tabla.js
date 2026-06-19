async function cargarTabla() {
  try {
    const tabla = await api.getTabla();
    renderTabla(tabla);
  } catch (err) {
    showToast(err.message, 'error');
  }
}

function renderTabla(tabla) {
  const cuerpo = document.getElementById('cuerpo-tabla');

  if (tabla.length === 0) {
    cuerpo.innerHTML = `<tr><td colspan="10" class="empty-state">Aún no hay equipos registrados.</td></tr>`;
    return;
  }

  cuerpo.innerHTML = tabla.map((eq, i) => `
    <tr class="${i === 0 ? 'leader' : ''}">
      <td>${i + 1}</td>
      <td class="al">${escapeHtml(eq.nombre)}</td>
      <td>${eq.partidos_jugados}</td>
      <td>${eq.ganados}</td>
      <td>${eq.empatados}</td>
      <td>${eq.perdidos}</td>
      <td>${eq.goles_favor}</td>
      <td>${eq.goles_contra}</td>
      <td>${eq.diferencia_goles > 0 ? '+' + eq.diferencia_goles : eq.diferencia_goles}</td>
      <td class="pts">${eq.puntos}</td>
    </tr>
  `).join('');
}