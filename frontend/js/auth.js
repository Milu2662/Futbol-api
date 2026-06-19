function mostrarLogin() {
  document.getElementById('login-screen').classList.remove('hidden');
  document.getElementById('app-root').classList.add('hidden');
}

function mostrarApp() {
  document.getElementById('login-screen').classList.add('hidden');
  document.getElementById('app-root').classList.remove('hidden');
}

async function verificarSesion() {
  if (getToken()) {
    mostrarApp();
    await cargarDatosIniciales();
  } else {
    mostrarLogin();
  }
}

document.getElementById('form-login').addEventListener('submit', async (e) => {
  e.preventDefault();
  const username = document.getElementById('input-username').value.trim();
  const password = document.getElementById('input-password').value;
  const errorEl = document.getElementById('login-error');
  errorEl.textContent = '';

  try {
    await login(username, password);
    document.getElementById('form-login').reset();
    mostrarApp();
    await cargarDatosIniciales();
  } catch (err) {
    errorEl.textContent = err.message;
  }
});

document.getElementById('btn-logout').addEventListener('click', () => {
  clearToken();
  showToast('Sesión cerrada.', 'success');
  mostrarLogin();
});