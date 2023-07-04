import hashlib
import json
import logging
import os
from flask import Flask, Response, render_template, request
from flask_cors import CORS, cross_origin
import filetype
from db_utils import Tarea2DB
from models import Donacion, Pedido
from utils import get_map_data, validate_conf_img
from werkzeug.utils import secure_filename

logging.getLogger().setLevel(logging.INFO)


UPLOAD_FOLDER = './static/uploads'


app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
CORS(app)
# app.config['SESSION_COOKIE_HTTPONLY'] = False


@app.route('/')
def index():
    try:
        return render_template("inicio.html")
    except Exception as e:
        logging.error(f"Error in index: {e}")
        return render_template("error.html")


@app.route('/ver-pedidos')
def ver_pedidos():
    try:
        args = request.args
        total_donaciones = Tarea2DB.get_total_rows('pedido')
        number_of_pages = range(1, total_donaciones // 5 + 1 + 1)
        if request.method == 'GET':
            page_request = request.args.get("page")
            request_page = 0 if not page_request or page_request=="1" else int(page_request)
            response = Tarea2DB.get_pedidos(page=request_page, page_size=5)
            print(response)
            for entry in response:
                comuna = Tarea2DB.get_comuna_by_id(entry.get("comuna_id"))
                comuna_nombre = comuna.get("nombre")
                entry["comuna_nombre"] = comuna_nombre
            print(response)
        return render_template("ver-pedidos.html", pedidos=response, page=request_page, total_pages=number_of_pages)
    except Exception as e:
        logging.error(f"Error in ver_pedidos: {e}")
        return Response(status=500, response=str(e))



@app.route('/agregar-donacion', methods=('GET', 'POST'))
def agregar_donacion():
    if request.method == 'POST':
        try:
            logging.info(f"Request: {request.form}")
        except Exception as e:
            logging.error(f"Error in agregar_donacion: {e}")
            return render_template("error.html")
    return render_template("agregar-donacion.html")


@app.route('/api/agregar-donacion', methods=['POST', 'OPTIONS'])
def api_agregar_donacion():
    """
    Receives a POST request with the form data and inserts it into the database.
    """
    if request.method == 'POST':
        try:
            donacion = Donacion(**request.form.to_dict())
            fotos = request.files.getlist("fotos")
            if len(fotos) == 0:
                raise Exception("Debe ingresar al menos una foto")
            # TODO VALIDATE FILES
            for foto in fotos:
                if not validate_conf_img(foto):
                    raise Exception(f"Archivo {foto.filename} no es una imagen valida")
            response_id = Tarea2DB.insert_donacion(donacion)
            print(response_id)
            if response_id:
                logging.info(f"Sucessfully inserted {donacion} in database")
                for foto in fotos:
                    filename = secure_filename(foto.filename)
                    _filename = hashlib.sha256(filename.encode("utf-8")).hexdigest()
                    _extension = filetype.guess(foto).extension
                    img_filename = f"{_filename}.{_extension}"
                    file_address = os.path.join(app.config["UPLOAD_FOLDER"], img_filename)
                    foto.save(file_address)
                    Tarea2DB.insert_foto(ruta_archivo=file_address,
                                         nombre_archivo=filename,
                                         donacion_id=response_id)
                return Response(status=204)
        except Exception as e:
            logging.error(f"Error in agregar_donacion: {e}")
            return Response(status=500, response=str(e))
    return Response(status=204)


@app.route('/agregar-pedido')
def agregar_pedido():
    if request.method == 'POST':
        try:
            logging.info(f"Request: {request.form}")
        except Exception as e:
            logging.error(f"Error in agregar_pedido: {e}")
            return render_template("error.html")
    return render_template("agregar-pedido.html")


@app.route('/api/agregar-pedido', methods=['POST'])
def api_agregar_pedido():
    if request.method == 'POST':
        try:
            pedido = Pedido(**request.form.to_dict())
            response = Tarea2DB.insert_pedido(pedido=pedido)
            if response:
                logging.info(f"Sucessfully inserted {pedido} in database")
                return Response(status=204)
        except Exception as e:
            logging.error(f"Error in validate_pedido: {e}")
            return Response(status=500, response=str(e))
    return Response(status=204)


@app.route('/ver-donaciones', methods= ['GET'])
def ver_donaciones():
    try:
        args = request.args
        total_donaciones = Tarea2DB.get_total_rows('donacion')
        number_of_pages = range(1, total_donaciones // 5 + 1 + 1)
        if request.method == 'GET':
            page_request = request.args.get("page")
            request_page = 0 if not page_request or page_request=="1" else int(page_request)
            response = Tarea2DB.get_donaciones(page=request_page, page_size=5)
            for entry in response:
                comuna = Tarea2DB.get_comuna_by_id(entry.get("comuna_id"))
                comuna_nombre = comuna.get("nombre")
                entry["comuna_nombre"] = comuna_nombre
            print(response)
        return render_template("ver-donaciones.html", donaciones=response, page=request_page, total_pages=number_of_pages)
    except Exception as e:
        logging.error(f"Error in ver_donaciones: {e}")
        return Response(status=500, response=str(e))


@app.route('/informacion-donacion/<donacion_id>', methods= ['GET'])
def informacion_donacion(donacion_id):
    try:
        donacion = Tarea2DB.get_donacion_by_id(donacion_id)
        comuna = Tarea2DB.get_comuna_by_id(donacion.get("comuna_id"))
        if comuna is None:
            raise Exception(f"Comuna {donacion.get('comuna_id')} para la donacion {donacion_id} no existe.")
        comuna_nombre = comuna.get("nombre")
        donacion["comuna_nombre"] = comuna_nombre
        region = Tarea2DB.get_region_nombre_by_comuna_id(donacion.get("comuna_id"))
        if region is None:
            raise Exception(f"Region para la comuna {donacion.get('comuna_id')} no existe.")
        region_nombre = region.get("nombre")
        donacion["region_nombre"] = region_nombre
        return render_template("informacion-donacion.html", donacion=donacion)
    except Exception as e:
        logging.error(f"Error in informacion_donacion: {e}")
        return Response(status=500, response=str(e))

@app.route('/informacion-pedido/<pedido_id>', methods= ['GET'])
def informacion_pedido(pedido_id):
    try:
        pedido = Tarea2DB.get_pedido_by_id(pedido_id)
        comuna = Tarea2DB.get_comuna_by_id(pedido.get("comuna_id"))
        region = Tarea2DB.get_region_nombre_by_comuna_id(pedido.get("comuna_id"))
        if comuna is None:
            raise Exception(f"Comuna {pedido.get('comuna_id')} para la donacion {pedido_id} no existe.")
        comuna_nombre = comuna.get("nombre")
        if region is None:
            raise Exception(f"Region para la comuna {pedido.get('comuna_id')} no existe.")
        region_nombre = region.get("nombre")
        pedido["comuna_nombre"] = comuna_nombre
        pedido["region_nombre"] = region_nombre
        return render_template("informacion-pedido.html", pedido=pedido)
    except Exception as e:
        logging.error(f"Error in informacion_pedido: {e}")
        return Response(status=500, response=str(e))

@app.route('/stats')
def stats():
    try:
        return render_template("stats.html")
    except Exception as e:
        logging.error(f"Error in stats: {e}")
        return Response(status=500, response=str(e))
    
@app.route("/get-stats-data", methods=["GET"])
@cross_origin(origin="localhost", supports_credentials=True)
def get_stats_data():
    data_donaciones_raw = Tarea2DB.get_count_by_tipo_donacion()
    data_donaciones = {}
    for entry in data_donaciones_raw:
        data_donaciones[entry.get("tipo")] = entry.get("count")
    data_pedidos_raw = Tarea2DB.get_count_by_tipo_pedido()
    data_pedidos = {}
    for entry in data_pedidos_raw:
        data_pedidos[entry.get("tipo")] = entry.get("count")
    chart_data = {
        "donaciones": data_donaciones,
        "pedidos": data_pedidos
    }
    return json.dumps(chart_data)

@app.route("/get-map-data", methods=["GET"])
@cross_origin(origin="localhost", supports_credentials=True)
def get_map_data_api():
    try:
        markers_donaciones, markers_pedidos = get_map_data()
        return json.dumps({
            "donaciones": markers_donaciones,
            "pedidos": markers_pedidos
        })
    except Exception as e:
        logging.error(f"Error in get_map_data_api: {e}")
        return Response(status=500, response=str(e))