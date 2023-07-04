import datetime
from db_utils import Tarea2DB
from enum import Enum
import logging
import re
from typing import Optional
from pydantic import BaseModel, validator
logging.getLogger().setLevel(logging.INFO)


class Tipo(str, Enum):
    fruta = "fruta"
    verdura = "verdura"
    otro = "otro"

class Donacion(BaseModel):
    region_id: int
    comuna_id: int
    comuna_nombre: Optional[str]
    calle_numero: str
    descripcion: Optional[str] = ""
    condiciones_retirar: Optional[str] = ""
    tipo: Tipo
    cantidad: int
    fecha_disponibilidad: str
    nombre: str
    email: str
    celular: str

    @validator('region_id')
    def validate_region_id(cls, v):
        regiones = Tarea2DB.get_regiones()
        for id, name in regiones:
            if int(id) == int(v):
                return v
        raise ValueError(f"Region {v} no existe.")

    @validator('comuna_id')
    def validate_comuna_id(cls, v, values, **kwargs):
        comunas = Tarea2DB.get_comunas_by_region_id(values['region_id'])
        for id, name, region_id in comunas:
            if int(id) == int(v):
                return v
        raise ValueError(f"Comuna {v} no existe.")

    @validator('email')
    def validate_email(cls, v):
        pattern=r"^[^\s@]+@[^\s@]+\.[^\s@]+$"
        if re.match(pattern, v):
            return v
        else:
            raise ValueError(f"Email {v} no es valido")

    @validator('celular')
    def validate_telefono(cls, v):
        pattern=r"^\+56(?:9)[1-9]\d{7}$"
        if re.match(pattern, v):
            return v
        else:
            raise ValueError(f"Celular {v} no es valido")
        
        
    @validator('fecha_disponibilidad')
    def validate_fecha(cls, v):
        try:
            fecha = datetime.datetime.strptime(v, "%Y-%m-%d")
            today = datetime.datetime.today()
            if today <= fecha:
                return fecha
        except Exception as e:
            raise ValueError(f"Error validando fecha-disponiblidad: {e}")
        
    @validator('nombre')
    def valide_nombre(cls, v):
        try:
            if 3 <= len(v) <= 80:
                return v
        except Exception as e:
            raise ValueError(f"Error validando nombre: {e}")

class Pedido(BaseModel):
    region_id: int
    comuna_id: int
    descripcion: str
    condiciones_retirar: Optional[str] = ""
    tipo: Tipo
    cantidad: int
    nombre_solicitante: str
    email_solicitante: str
    celular_solicitante: str

    @validator('region_id')
    def validate_region_id(cls, v):
        regiones = Tarea2DB.get_regiones()
        for id, name in regiones:
            if int(id) == int(v):
                return v
        raise ValueError(f"Region {v} no existe.")
    
    @validator('comuna_id')
    def validate_comuna_id(cls, v, values, **kwargs):
        comunas = Tarea2DB.get_comunas_by_region_id(values['region_id'])
        for id, name, region_id in comunas:
            if int(id) == int(v):
                return v
        raise ValueError(f"Comuna {v} no existe.")
    
    @validator('email_solicitante')
    def validate_email(cls, v):
        pattern=r"^[^\s@]+@[^\s@]+\.[^\s@]+$"
        if re.match(pattern, v):
            return v
        else:
            raise ValueError(f"Email {v} no es valido")
        
    @validator('celular_solicitante')
    def validate_celular(cls, v):
        pattern=r"^\+56(?:9)[1-9]\d{7}$"
        if re.match(pattern, v):
            return v
        else:
            raise ValueError(f"Celular {v} no es valido")
        
    @validator('nombre_solicitante')
    def validate_nombre(cls, v):
        try:
            if 3 <= len(v) <= 80:
                return v
        except Exception as e:
            raise ValueError(f"Error validando nombre: {e}")
        
    @validator('descripcion')
    def validate_description(cls, v):
        try:
            if len (v) <= 250:
                return v
        except Exception as e:
            raise ValueError(f"Error validando descripcion: {e}")