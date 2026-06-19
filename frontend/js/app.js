async function cargarDatosIniciales() {
  await cargarEquipos();
  await cargarPartidos();
  await cargarTabla();
}

document.addEventListener('DOMContentLoaded', async () => {
  initTabs();
  await verificarSesion();
});