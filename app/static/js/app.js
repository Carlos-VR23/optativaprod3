// app/static/js/app.js

// ---------- Mensajes (flash) ----------
function showFlash(text, type = "success") {
  const flash = document.getElementById("flash");
  if (!flash) return;
  flash.textContent = text;
  flash.className = `flash flash-${type}`;
  flash.hidden = false;
}

// Mensaje que viene en la URL después de eliminar (/?msg=deleted)
const msgParam = new URLSearchParams(window.location.search).get("msg");
if (msgParam === "deleted") {
  showFlash("Restaurante eliminado correctamente");
  history.replaceState({}, "", window.location.pathname);
}

// Convierte la respuesta de error de FastAPI en texto legible
function formatError(error) {
  if (!error || !error.detail) return "Error al guardar";
  if (typeof error.detail === "string") return error.detail;
  if (Array.isArray(error.detail)) {
    return error.detail
      .map((e) => `${(e.loc || []).slice(1).join(".")}: ${e.msg}`)
      .join(" | ");
  }
  return "Error al guardar";
}

// ---------- Formulario crear / editar ----------
const form = document.getElementById("restaurant-form");

if (form) {
  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    const message = document.getElementById("message");
    const isEdit = form.dataset.mode === "edit";

    const data = Object.fromEntries(new FormData(form));
    data.price = Number(data.price);
    data.photoUrl = data.photoUrl && data.photoUrl.trim() ? data.photoUrl.trim() : null;

    const url = isEdit
      ? `/api/v1/restaurants/${form.dataset.id}`
      : "/api/v1/restaurants";

    message.className = "form-message";
    message.textContent = "Guardando…";

    try {
      const response = await fetch(url, {
        method: isEdit ? "PATCH" : "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data),
      });

      if (response.ok) {
        const saved = await response.json();
        message.className = "form-message ok";
        message.textContent = isEdit
          ? "Restaurante actualizado correctamente"
          : "Restaurante creado correctamente";
        setTimeout(() => {
          window.location.href = `/restaurants/${saved.id}`;
        }, 900);
      } else {
        const error = await response.json().catch(() => null);
        message.className = "form-message error";
        message.textContent = formatError(error);
      }
    } catch (err) {
      message.className = "form-message error";
      message.textContent = "No se pudo conectar con el servidor";
    }
  });
}

// ---------- Eliminar desde el detalle ----------
const deleteBtn = document.getElementById("delete-btn");

if (deleteBtn) {
  deleteBtn.addEventListener("click", async () => {
    const name = deleteBtn.dataset.name;
    if (!confirm(`¿Seguro que quieres eliminar "${name}"? Esta acción no se puede deshacer.`)) {
      return;
    }
    try {
      const response = await fetch(`/api/v1/restaurants/${deleteBtn.dataset.id}`, {
        method: "DELETE",
      });
      if (response.status === 204) {
        window.location.href = "/?msg=deleted";
      } else {
        const error = await response.json().catch(() => null);
        showFlash(formatError(error), "error");
      }
    } catch (err) {
      showFlash("No se pudo conectar con el servidor", "error");
    }
  });
}
