export function setText(id, value) {
  const el = document.getElementById(id);
  if (el) el.textContent = String(value);
}
