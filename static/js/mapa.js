/* mapa.js – carga Leaflet y dibuja los dos marcadores */

document.addEventListener('DOMContentLoaded', function () {
  // MAP_DATA está inyectado en la plantilla mediante json_script
  const data = window.MAP_DATA;
  if (!data || !data.solicitante || !data.propietario) {
    const el = document.getElementById('mapa');
    if (el) el.innerHTML = '<p class="text-center">Información de ubicación no disponible.</p>';
    return;
  }

  const s = data.solicitante;
  const p = data.propietario;

  // Si alguna coordenada es null, avisar al usuario
  if (!s.lat || !s.lng || !p.lat || !p.lng) {
    const el = document.getElementById('mapa');
    if (el) el.innerHTML = '<p class="text-center">Alguno de los usuarios no ha registrado su ubicación.</p>';
    return;
  }

  const centerLat = (parseFloat(s.lat) + parseFloat(p.lat)) / 2;
  const centerLng = (parseFloat(s.lng) + parseFloat(p.lng)) / 2;

  const map = L.map('mapa').setView([centerLat, centerLng], 12);

  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://openstreetmap.org">OpenStreetMap</a> contributors',
    maxZoom: 19,
  }).addTo(map);

  const userIcon = L.icon({
    iconUrl: '/static/img/user.svg',
    iconSize: [30, 30],
    iconAnchor: [15, 30],
    popupAnchor: [0, -30],
  });
  const bookIcon = L.icon({
    iconUrl: '/static/img/book.svg',
    iconSize: [30, 30],
    iconAnchor: [15, 30],
    popupAnchor: [0, -30],
  });

  L.marker([s.lat, s.lng], { icon: userIcon })
    .bindPopup(`<strong>${s.name}</strong> (tú)`).addTo(map);
  L.marker([p.lat, p.lng], { icon: bookIcon })
    .bindPopup(`<strong>${p.name}</strong> (propietario)`).addTo(map);

  const line = L.polyline([[s.lat, s.lng], [p.lat, p.lng]], {
    color: getComputedStyle(document.documentElement).getPropertyValue('--primary').trim(),
    weight: 3,
  }).addTo(map);

  const distanceMeters = map.distance([s.lat, s.lng], [p.lat, p.lng]);
  const mid = line.getBounds().getCenter();
  L.popup()
    .setLatLng(mid)
    .setContent(`<strong>Distancia aproximada:</strong> ${(distanceMeters / 1000).toFixed(2)} km`)
    .openOn(map);
});
