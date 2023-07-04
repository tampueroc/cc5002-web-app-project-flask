
let map = L.map("map").setView([-33.457925, -70.664511], 13);

L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png", {
  maxZoom: 19,
  attribution:
    '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>',
}).addTo(map);

function load_donaciones_in_map(map_data) {
  console.log(map_data);
  for (let comuna of map_data) {
    let comuna_entries = comuna.entries;
    console.log(comuna_entries);
    let lat = comuna["comuna_lat"];
    let lng = comuna["comuna_long"];
    const onMarkerClick = (e) => {
      L.popup()
        .setLatLng([lat, lng])
        .setContent(get_donacion_html(comuna_entries))
        .openOn(map);
    };

    let marker = L.marker([lat, lng]).addTo(map);
    marker.on("click", onMarkerClick);
  }
}
function get_donacion_html(entry) {
  let html = "";
  for (let e of entry) {
    html += "<h6>Donacion #" + e.id + "</h6>" + "calle: " + e.calle_numero + "<br>" + "tipo: " +  e.tipo + "<br>" + "cantidad: "+ e.cantidad + "<br> fecha_disponibilidad: " + e.fecha_disponibilidad + "<br> email:" + e.email + "<br>";
  }
  return html;
}
function get_pedido_html(entry) {
  let html = "";
  for (let e of entry) {
    html += "<h6>Pedido #" + e.id + "</h6>" + "tipo: " + e.tipo + "<br>" + "cantidad: " +  e.cantidad + "<br> email_solicitante:" + e.email_solicitante + "<br>";
  }
  return html;
}
function load_pedidos_in_map(map_data) {
  for (let comuna of map_data) {
    let comuna_entries = comuna["entries"];
    let lat = comuna["comuna_lat"];
    let lng = comuna["comuna_long"];
    const onMarkerClick = (e) => {
      L.popup()
        .setLatLng([lat, lng])
        .setContent(get_pedido_html(comuna_entries))
        .openOn(map);
    };

    let marker = L.marker([lat, lng]).addTo(map);
    marker._icon.style.filter = "hue-rotate(120deg)"
    marker.on("click", onMarkerClick);
  }
}
function populate_map_donaciones() {
    fetch("http://localhost:5000/get-map-data")
    .then((response) => response.json())
    .then((data) => {
        console.log(data);
        let markers_donaciones = data.donaciones;
        load_donaciones_in_map(markers_donaciones)
        let markers_pedidos = data.pedidos;
        load_pedidos_in_map(markers_pedidos)
    });
}
populate_map_donaciones();