let equiposCache = [];

async function cargarEquipos() {
  try {
    equiposCache = await api.getEquipos();
    renderEquipos();
  } catch (err) {
    showToast(err.message, 'error');
  }
}

function renderEquipos() {
  const lista = document.getElementById('lista-equipos');
  const slots = document.getElementById('slots-equipos');

  slots.innerHTML = [0, 1, 2, 3]
    .map(i => `<span class="slot ${i < equiposCache.length ? 'filled' : ''}"></span>`)
    .join('');

  if (equiposCache.length === 0) {
    lista.innerHTML = `<li class="empty-state">Aún no hay equipos registrados. Agrega el primero arriba.</li>`;
    return;
  }

  lista.innerHTML = equiposCache.map(eq => `
    <li class="team-row" data-id="${eq.id}">
      <span class="team-avatar">${escapeHtml(eq.nombre.charAt(0).toUpperCase())}</span>
      <span class="team-name" data-view="${eq.id}">${escapeHtml(eq.nombre)}</span>
      <input class="team-edit-input hidden" data-edit="${eq.id}" value="${escapeHtml(eq.nombre)}" maxlength="100">
      <span class="team-row-actions">
        <button class="btn btn-ghost btn-small" data-action="editar" data-id="${eq.id}">Editar</button>
        <button class="btn btn-pitch btn-small hidden" data-action="guardar" data-id="${eq.id}">Guardar</button>
        <button class="btn btn-ghost btn-small hidden" data-action="cancelar" data-id="${eq.id}">Cancelar</button>
        <button class="btn btn-danger btn-small" data-action="eliminar" data-id="${eq.id}">Eliminar</button>
      </span>
    </li>
  `).join('');
}

document.addEventListener('click', async (e) => {
  const btn = e.target.closest('button[data-action]');
  if (!btn) return;
  const row = btn.closest('.team-row');
  if (!row) return;

  const id = Number(btn.dataset.id);
  const nameView = row.querySelector('[data-view]');
  const nameInput = row.querySelector('[data-edit]');
  const editBtn = row.querySelector('[data-action="editar"]');
  const saveBtn = row.querySelector('[data-action="guardar"]');
  const cancelBtn = row.querySelector('[data-action="cancelar"]');

  if (btn.dataset.action === 'editar') {
    nameView.classList.add('hidden');
    nameInput.classList.remove('hidden');
    editBtn.classList.add('hidden');
    saveBtn.classList.remove('hidden');
    cancelBtn.classList.remove('hidden');
    nameInput.focus();
  }

  if (btn.dataset.action === 'cancelar') {
    nameInput.value = nameView.textContent;
    nameView.classList.remove('hidden');
    nameInput.classList.add('hidden');
    editBtn.classList.remove('hidden');
    saveBtn.classList.add('hidden');
    cancelBtn.classList.add('hidden');
  }

  if (btn.dataset.action === 'guardar') {
    const nuevoNombre = nameInput.value.trim();
    if (!nuevoNombre) return;
    try {
      await api.actualizarEquipo(id, nuevoNombre);
      showToast('Equipo actualizado.', 'success');
      await cargarEquipos();
      await cargarPartidos();
      await cargarTabla();
    } catch (err) {
      showToast(err.message, 'error');
    }
  }

  if (btn.dataset.action === 'eliminar') {
    const nombreEquipo = nameView.textContent;
    const confirmado = confirm(`¿Eliminar "${nombreEquipo}"? Esto también borra sus partidos asociados.`);
    if (!confirmado) return;

    try {
      await api.eliminarEquipo(id);
      showToast('Equipo eliminado.', 'success');
      await cargarEquipos();
      await cargarPartidos();
      await cargarTabla();
    } catch (err) {
      showToast(err.message, 'error');
    }
  }
});

document.getElementById('form-equipo').addEventListener('submit', async (e) => {
  e.preventDefault();
  const input = document.getElementById('input-nombre-equipo');
  const nombre = input.value.trim();
  if (!nombre) return;
  try {
    await api.crearEquipo(nombre);
    input.value = '';
    showToast('Equipo registrado.', 'success');
    await cargarEquipos();
  } catch (err) {
    showToast(err.message, 'error');
  }
});

document.getElementById('btn-reiniciar-torneo').addEventListener('click', async () => {
  const confirmado = confirm('¿Seguro que quieres reiniciar el torneo? Esto borra todos los equipos y partidos.');
  if (!confirmado) return;

  try {
    await api.reiniciarTorneo();
    showToast('Torneo reiniciado.', 'success');
    await cargarEquipos();
    await cargarPartidos();
    await cargarTabla();
  } catch (err) {
    showToast(err.message, 'error');
  }
});