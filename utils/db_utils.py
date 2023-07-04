import logging
import pymysql


logging.getLogger().setLevel(logging.INFO)



class Tarea2DB:

    _db = pymysql.connect(
        db='tarea2',
        user='cc5002',
        passwd='programacionweb',
        host='localhost',
        port=3306
    )

    @classmethod
    def get_regiones(cls):
        """
        Get all entries from 'region' table
        """
        try:
            cursor = cls._db.cursor()
            cursor.execute("SELECT * FROM region;")
            return cursor.fetchall()
        except Exception as e:
            logging.error(f"Error in DB.get_regiones: {e}")
            return None
        
    @classmethod
    def get_comunas_by_region_id(cls, region_id):
        """
        Get all comunas by region_id
        """
        try:
            cursor = cls._db.cursor()
            cursor.execute(f"SELECT * FROM comuna WHERE region_id={region_id};")
            return cursor.fetchall()
        except Exception as e:
            logging.error(f"Error in DB.get_comunas_by_region_id: {e}")
            return None
        

    @classmethod
    def get_comuna_by_id(cls, comuna_id):
        """
        Get comuna by id
        """
        try:
            cursor = cls._db.cursor(pymysql.cursors.DictCursor)
            cursor.execute(f"SELECT nombre FROM comuna WHERE id={comuna_id};")
            return cursor.fetchone()
        except Exception as e:
            logging.error(f"Error in DB.get_comuna_by_id: {e}")
            return None
        

    @classmethod
    def insert_donacion(cls, donacion):
        """
        Insert Donacion in the database
        """
        try:
            cursor = cls._db.cursor()
            values = [donacion.comuna_id,
                      donacion.calle_numero, 
                      donacion.tipo.value, 
                      donacion.cantidad, 
                      donacion.fecha_disponibilidad, 
                      donacion.descripcion,
                      donacion.condiciones_retirar, 
                      donacion.nombre, 
                      donacion.email, 
                      donacion.celular]
            # Tranform every value to str
            values = [str(v) for v in values]
            logging.info(f"Values: {values}")
            logging.info(f"Len values: {len(values)}")
            sentencia = "INSERT INTO donacion (comuna_id, calle_numero, tipo, cantidad, fecha_disponibilidad, descripcion, condiciones_retirar, nombre, email, celular) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
            response = cursor.execute(sentencia, values)
            cls._db.commit()
            return cursor.lastrowid
        except Exception as e:
            logging.error(f"Error in DB.insert_donacion: {e}")
            raise e


    @classmethod
    def insert_pedido(cls, pedido):
        """
        Insert Pedido in the database
        """
        try:
            cursor = cls._db.cursor()
            values = [pedido.comuna_id,
                      pedido.descripcion,
                      pedido.tipo.value,
                      pedido.cantidad,
                      pedido.nombre_solicitante,
                      pedido.email_solicitante,
                      pedido.celular_solicitante]
            values = [str(v) for v in values]
            sentencia = "INSERT INTO pedido (comuna_id, descripcion, tipo, cantidad, nombre_solicitante, email_solicitante, celular_solicitante) VALUES (%s, %s, %s, %s, %s, %s, %s);"
            response = cursor.execute(sentencia, values)
            cls._db.commit()
            return cursor.lastrowid
        except Exception as e:
            logging.error(f"Error in DB.insert_pedido: {e}")
            raise e

    @classmethod
    def get_total_rows(cls, table):
        """
        Get total rows from table
        """
        try:
            cursor = cls._db.cursor()
            cursor.execute(f"SELECT COUNT(*) FROM {table};")
            return cursor.fetchone()[0]
        except Exception as e:
            logging.error(f"Error in DB.get_total_rows: {e}")
            return None


    @classmethod
    def get_donaciones(cls, page, page_size):
        """
        Get 5 latest donations
        """
        try:
            cursor = cls._db.cursor(pymysql.cursors.DictCursor)
            donaciones = []
            if page>1:
                page -= 1
            sentencia = f"SELECT id, comuna_id, tipo, email, calle_numero, cantidad, fecha_disponibilidad, nombre FROM donacion ORDER BY id DESC LIMIT {str(page_size)} OFFSET {str(page*page_size)};"
            print(sentencia)
            # sentencia = f"SELECT id, comuna_id, calle_numero, tipo, cantidad, fecha_disponibilidad, descripcion, condiciones_retirar, nombre, email, celular FROM donacion ORDER BY id DESC LIMIT {page*page_size}, {(page+1)*page_size};"
            cursor.execute(sentencia)
            donaciones = cursor.fetchall()
            return donaciones
        except Exception as e:
            logging.error(f"Error in DB.get_donaciones: {e}")
            return None
        
    @classmethod
    def get_donacion_by_id(cls, donacion_id):
        """
        Get donacion by id
        """
        try:
            cursor = cls._db.cursor(pymysql.cursors.DictCursor)
            cursor.execute(f"SELECT * FROM donacion WHERE id={donacion_id};")
            return cursor.fetchone()
        except Exception as e:
            logging.error(f"Error in DB.get_donacion_by_id: {e}")
            return None
    
    @classmethod
    def get_region_by_id(cls, region_id):
        """
        Get region by id
        """
        try:
            cursor = cls._db.cursor(pymysql.cursors.DictCursor)
            cursor.execute(f"SELECT * FROM region WHERE id={region_id};")
            return cursor.fetchone()
        except Exception as e:
            logging.error(f"Error in DB.get_region_by_id: {e}")
            return None
        
    @classmethod
    def insert_foto(cls, ruta_archivo, nombre_archivo, donacion_id):
        try:
            cursor = cls._db.cursor()
            values = [ruta_archivo, nombre_archivo, donacion_id]
            values = [str(v) for v in values]
            sentencia = "INSERT INTO foto (ruta_archivo, nombre_archivo, donacion_id) VALUES (%s, %s, %s);"
            response = cursor.execute(sentencia, values)
            cls._db.commit()
            return True
        except Exception as e:
            logging.error(f"Error in DB.insert_foto: {e}")
            raise e
        
    @classmethod
    def get_pedidos(cls, page, page_size):
        """
        Get 5 latest pedidos
        """
        try:
            cursor = cls._db.cursor(pymysql.cursors.DictCursor)
            pedidos = []
            if page>1:
                page -= 1
            sentencia = f"SELECT id, comuna_id, tipo, cantidad, descripcion, nombre_solicitante FROM pedido ORDER BY id DESC LIMIT {str(page_size)} OFFSET {str(page*page_size)};"
            cursor.execute(sentencia)
            pedidos = cursor.fetchall()
            return pedidos
        except Exception as e:
            logging.error(f"Error in DB.get_pedidos: {e}")
            return None
    
    @classmethod
    def get_pedido_by_id(cls, pedido_id):
        """
        Get pedido by id
        """
        try:
            cursor = cls._db.cursor(pymysql.cursors.DictCursor)
            cursor.execute(f"SELECT * FROM pedido WHERE id={pedido_id};")
            return cursor.fetchone()
        except Exception as e:
            logging.error(f"Error in DB.get_pedido_by_id: {e}")
            return None
        
    @classmethod
    def get_region_nombre_by_comuna_id(cls, comuna_id):
        """
        Get region by comuna_id using inner join
        """
        try:
            cursor = cls._db.cursor(pymysql.cursors.DictCursor)
            cursor.execute(f"SELECT region.nombre FROM region INNER JOIN comuna ON region.id = comuna.region_id WHERE comuna.id = {comuna_id};")
            return cursor.fetchone()
        except Exception as e:
            logging.error(f"Error in DB.get_region_nombre_by_comuna_id: {e}")
            return None
    
    @classmethod
    def get_count_by_tipo_donacion(cls):
        """
        Get count by tipo donacion
        """
        try:
            cursor = cls._db.cursor(pymysql.cursors.DictCursor)
            cursor.execute("SELECT tipo, COUNT(*) AS count FROM donacion GROUP BY tipo;")
            return cursor.fetchall()
        except Exception as e:
            logging.error(f"Error in DB.get_count_by_tipo_donacion: {e}")
            return None

    @classmethod
    def get_count_by_tipo_pedido(cls):
        """
        Get count by tipo donacion
        """
        try:
            cursor = cls._db.cursor(pymysql.cursors.DictCursor)
            cursor.execute("SELECT tipo, COUNT(*) AS count FROM pedido GROUP BY tipo;")
            return cursor.fetchall()
        except Exception as e:
            logging.error(f"Error in DB.get_count_by_tipo_donacion: {e}")
            return None