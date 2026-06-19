document.addEventListener('DOMContentLoaded', async () => {
  initTabs();
  await cargarEquipos();
  await cargarPartidos();
  await cargarTabla();
});