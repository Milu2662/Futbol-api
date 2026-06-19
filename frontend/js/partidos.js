async function cargarPartidos() {
  try {
    const partidos = await api.getPartidos();
    renderPartidos(partidos);
  } catch (err) {
    showToast(err.message, 'error');
  }
}

function renderPartidos(partidos) {
  const contenedor = document.getElementById('lista-partidos');
  const btnFixture = document.getElementById('btn-generar-fixture');

  btnFixture.classList.toggle('hidden', partidos.length > 0);

  if (partidos.length === 0) {
    contenedor.innerHTML = `<p class="empty-state">Registra 4 equipos en la pestaña Equipos y genera el fixture para ver los partidos aquí.</p>`;
    return;
  }

  contenedor.innerHTML = partidos.map(p => `
    <article class="match-card" data-id="${p.id}">
      <div class="match-teams">
        <span class="match-team">${escapeHtml(p.equipo_local.nombre)}</span>
        <span class="match-vs">vs</span>
        <span class="match-team">${escapeHtml(p.equipo_visitante.nombre)}</span>
      </div>
      <div class="match-score">
        <input type="number" min="0" class="score-input" data-side="local" value="${p.goles_local ?? ''}">
        <span class="divider">–</span>
        <input type="number" min="0" class="score-input" data-side="visitante" value="${p.goles_visitante ?? ''}">
      </div>
      <div class="match-actions">
        <span class="badge ${p.jugado ? 'jugado' : 'pendiente'}">${p.jugado ? 'Jugado' : 'Pendiente'}</span>
        <button class="btn btn-pitch btn-small" data-action="guardar-marcador">Guardar</button>
      </div>
    </article>
  `).join('');
}

document.getElementById('btn-generar-fixture').addEventListener('click', async () => {
  try {
    await api.generarFixture();
    showToast('Fixture generado: 6 partidos creados.', 'success');
    await cargarPartidos();
  } catch (err) {
    showToast(err.message, 'error');
  }
});

document.getElementById('lista-partidos').addEventListener('click', async (e) => {
  const btn = e.target.closest('button[data-action="guardar-marcador"]');
  if (!btn) return;
  const card = btn.closest('.match-card');
  const id = Number(card.dataset.id);
  const golesLocal = card.querySelector('[data-side="local"]').value;
  const golesVisitante = card.querySelector('[data-side="visitante"]').value;

  if (golesLocal === '' || golesVisitante === '') {
    showToast('Ingresa ambos marcadores.', 'error');
    return;
  }

  try {
    await api.actualizarMarcador(id, Number(golesLocal), Number(golesVisitante));
    showToast('Marcador guardado.', 'success');
    await cargarPartidos();
    await cargarTabla();
  } catch (err) {
    showToast(err.message, 'error');
  }
});