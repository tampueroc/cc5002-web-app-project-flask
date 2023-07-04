import json
import filetype
import requests

from utils.db_utils import Tarea2DB

def validate_conf_img(conf_img):
    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}
    ALLOWED_MIMETYPES = {"image/jpeg", "image/png", "image/gif"}

    # check if a file was submitted
    if conf_img is None:
        return False

    # check if the browser submitted an empty file
    if conf_img.filename == "":
        return False
    
    # check file extension
    ftype_guess = filetype.guess(conf_img)
    if ftype_guess.extension not in ALLOWED_EXTENSIONS:
        return False
    # check mimetype
    if ftype_guess.mime not in ALLOWED_MIMETYPES:
        return False
    return True

def get_comuna_coordinates(comuna):
    comuna_coords = requests.get(f"https://raw.githubusercontent.com/tampueroc/cc5002-tareas-resources/main/tarea_1/comunas_chile_coords.json")
    comuna_coords = json.loads(comuna_coords.text)
    for comuna_coord in comuna_coords:
        if comuna_coord.get("name") == comuna:
            return comuna_coord.get("lat"), comuna_coord.get("lng")
        

def get_map_data():
    # Get last 5 donaciones
    donaciones = Tarea2DB.get_donaciones(page=0, page_size=5)
    donaciones_by_comuna = {}
    for entry in donaciones:
        comuna = Tarea2DB.get_comuna_by_id(entry.get("comuna_id"))
        comuna_nombre = comuna.get("nombre")
        entry["comuna_nombre"] = comuna_nombre
        entry["type"] = "donacion"
        entry["fecha_disponibilidad"] = entry.get("fecha_disponibilidad").strftime("%d/%m/%Y")
        if comuna_nombre in donaciones_by_comuna:
            donaciones_by_comuna[comuna_nombre].append(entry)
        else:
            donaciones_by_comuna[comuna_nombre] = [entry]

    # Get last 5 pedidos
    pedidos = Tarea2DB.get_pedidos(page=0, page_size=5)
    pedidos_by_comuna = {}
    for entry in pedidos:
        comuna = Tarea2DB.get_comuna_by_id(entry.get("comuna_id"))
        comuna_nombre = comuna.get("nombre")
        entry["comuna_nombre"] = comuna_nombre
        if comuna_nombre in pedidos_by_comuna:
            pedidos_by_comuna[comuna_nombre].append(entry)
        else:
            pedidos_by_comuna[comuna_nombre] = [entry]
    markers_donaciones = []
    for comuna in donaciones_by_comuna.keys():
        lat, lng = get_comuna_coordinates(comuna)
        markers_donaciones.append({
            "comuna_lat": lat,
            "comuna_long": lng,
            "entries": donaciones_by_comuna[comuna]
        })
    markers_pedidos= []
    for comuna in pedidos_by_comuna.keys():
        lat, lng = get_comuna_coordinates(comuna)
        markers_pedidos.append({
            "comuna_lat": lat if not donaciones_by_comuna.get(comuna) else float(lat) + 0.0025,
            "comuna_long": lng if not donaciones_by_comuna.get(comuna) else float(lng) + 0.0025,
            "entries": pedidos_by_comuna[comuna]
        })
    return markers_donaciones, markers_pedidos
