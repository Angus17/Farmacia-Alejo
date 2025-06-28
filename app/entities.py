"""
Este archivo contiene la definición de las entidades de la base de datos para la aplicación Flask.
Cada clase representa una tabla en la base de datos y sus atributos representan las columnas de la tabla.
Se utiliza SQLAlchemy como ORM para interactuar con la base de datos MySQL.
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
import secrets
from flask_migrate import Migrate


app = Flask(__name__)


# Aqui se configura la conexión a MySQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:ScNYZugUNlyWRAAQgKvEIVsXKtYWaQQh@trolley.proxy.rlwy.net:30856/farmacia_alejo' #f'mysql+pymysql://root:{os.getenv("PASSWDBD")}@localhost/farmacia_alejo'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['SECRET_KEY'] = secrets.token_hex(16)  # Genera una clave secreta aleatoria

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Pais(db.Model):
    __tablename__ = 'Pais'  # nombre exacto de la tabla en tu base de datos

    id_pais = db.Column(db.Integer, primary_key=True)
    nombre_pais = db.Column(db.String(100), nullable=False)
    clave_pais = db.Column(db.String(20), nullable=True)

class Estado(db.Model):
    __tablename__ = 'Estado'  # nombre exacto de la tabla en tu base de datos

    id_estado = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    clave_estado = db.Column(db.String(10), nullable=True)
    
    id_pais = db.Column(db.Integer, db.ForeignKey('Pais.id_pais'), nullable=True)  # Cambias a NOT NULL en MySQL
    pais = db.relationship('Pais')
    
class Municipio(db.Model):
    __tablename__ = 'Municipio'  # nombre exacto de la tabla en tu base de datos

    id_municipio = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    clave_municipio = db.Column(db.Integer, nullable=True)
    
    id_estado = db.Column(db.Integer, db.ForeignKey('Estado.id_estado'), nullable=True)  # Cambias a NOT NULL en MySQL

    estado = db.relationship('Estado')

class Tipos_Colonias(db.Model):
    __tablename__ = 'Tipos_Colonias'  # nombre exacto de la tabla en tu base de datos

    id_tipo_colonia = db.Column(db.Integer, primary_key=True)
    nombre_colonia = db.Column(db.String(100), nullable=False)

class Servicio(db.Model):
    __tablename__ = 'Servicio'  # nombre exacto de la tabla en tu base de datos

    id_servicio = db.Column(db.Integer, primary_key=True)
    nombre_servicio = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text, nullable=False)
    precio = db.Column(db.Numeric(10,2), nullable=False)
    duracion_estimada = db.Column(db.Time, nullable=False)  # en minutos
    
class FormasDePago(db.Model):
    __tablename__ = 'Formas_de_pago'  # nombre exacto de la tabla en tu base de datos

    id_pago = db.Column(db.Integer, primary_key=True)
    tipo_pago = db.Column(db.String(50), nullable=False)
    fecha_pago = db.Column(db.Date, nullable=False)
    
class DetallePago(db.Model):
    __tablename__ = 'Detalle_Pago'  # nombre exacto de la tabla en tu base de datos

    id_detalle_pago = db.Column(db.Integer, primary_key=True)
    tarjeta_digitos = db.Column(db.Integer, nullable=True)
    pagado = db.Column(db.Boolean, nullable=False, default=False)
    id_pago = db.Column(db.Integer, db.ForeignKey('Formas_de_pago.id_pago'), nullable=False)
    
    pago = db.relationship('FormasDePago')

class Sucursal(db.Model):
    __tablename__ = 'Sucursal'  # nombre exacto de la tabla en tu base de datos

    id_sucursal = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    direccion = db.Column(db.String(300), nullable=False)
    telefono = db.Column(db.String(50), nullable=False)

class Areas(db.Model):
    __tablename__ = 'Areas'  # nombre exacto de la tabla en tu base de datos
    
    id_area = db.Column(db.Integer, primary_key=True)
    nombre_area = db.Column(db.String(100), nullable=False)

class Rol(db.Model):
    __tablename__ = 'Rol'  # nombre exacto de la tabla en tu base de datos
    
    id_rol = db.Column(db.Integer, primary_key=True)
    tipo_rol = db.Column(db.String(50), nullable=False)

class Paciente(db.Model):
    __tablename__ = 'Paciente'  # nombre exacto de la tabla en tu base de datos
    
    id_paciente = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    segundo_nombre = db.Column(db.String(100), nullable=True)
    apellido = db.Column(db.String(100), nullable=False)
    segundo_apellido = db.Column(db.String(100), nullable=True)
    edad = db.Column(db.Integer, nullable=False)
    calle = db.Column(db.String(100), nullable=False)
    numero_exterior = db.Column(db.String(10), nullable=False)
    numero_interior = db.Column(db.String(10), nullable=True)
    codigo_postal = db.Column(db.String(10), nullable=False) #Cambias a NOT NULL en MySQL
    nombre_colonia = db.Column(db.String(100), nullable=False)
    numero_telefono = db.Column(db.String(15), nullable=False)
    numero_celular = db.Column(db.String(15), nullable=True)
    correo_electronico = db.Column(db.String(100), nullable=True)
    id_municipio = db.Column(db.Integer, db.ForeignKey('Municipio.id_municipio'), nullable=True)  # Cambias a NOT NULL en MySQL
    id_tipo_colonia = db.Column(db.Integer, db.ForeignKey('Tipos_Colonias.id_tipo_colonia'), nullable=True)  # Cambias a NOT NULL en MySQL

    municipio = db.relationship('Municipio')
    tipo_colonia = db.relationship('Tipos_Colonias')

class Empleado(db.Model):
    
    __tablename__ = 'Empleado'  # nombre exacto de la tabla en tu base de datos
    
    id_empleado = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    segundo_nombre = db.Column(db.String(100), nullable=True)
    apellido = db.Column(db.String(100), nullable=False)
    segundo_apellido = db.Column(db.String(100), nullable=True)
    fecha_contratacion = db.Column(db.Date, nullable=False)
    salario = db.Column(db.Numeric(10,2), nullable=False)
    prestaciones = db.Column(db.Text, nullable=True)
    calle = db.Column(db.String(100), nullable=False)
    numero_exterior = db.Column(db.String(100), nullable=True)
    numero_interior = db.Column(db.String(100), nullable=True)
    codigo_postal = db.Column(db.String(100), nullable=False)
    nombre_colonia = db.Column(db.String(100), nullable=False)
    
    
    id_sucursal = db.Column(db.Integer, db.ForeignKey('Sucursal.id_sucursal'), nullable=True)
    id_area = db.Column(db.Integer, db.ForeignKey('Areas.id_area'), nullable=True)
    id_tipo_colonia = db.Column(db.Integer, db.ForeignKey('Tipos_Colonias.id_tipo_colonia'), nullable=False)
    id_municipio = db.Column(db.Integer, db.ForeignKey('Municipio.id_municipio'), nullable=False)
    
    sucursal = db.relationship('Sucursal')
    area = db.relationship('Areas')
    tipo_colonia = db.relationship('Tipos_Colonias')
    municipio = db.relationship('Municipio')
    
class Doctor(db.Model):
    __tablename__ = 'Doctor'  # nombre exacto de la tabla en tu base de datos

    id_doctor = db.Column(db.Integer, primary_key=True)
    cedula_profesional = db.Column(db.String(100), nullable=False)
    especialidad = db.Column(db.String(50), nullable=True)
    
    id_empleado = db.Column(db.Integer, db.ForeignKey('Empleado.id_empleado'), nullable=False) # Recordar cambiar en MySQL que no es NULL
    empleado = db.relationship('Empleado')
    
class CitasDisponibles(db.Model):
    __tablename__ = 'Citas_Disponibles'  # nombre exacto de la tabla en tu base de datos

    id_cita_disponibles = db.Column(db.Integer, primary_key=True)
    fecha_disponible = db.Column(db.Date, nullable=False)
    hora_disponible = db.Column(db.Time, nullable=False)
    disponible = db.Column(db.Boolean, nullable=True, default=True)
    
    id_doctor = db.Column(db.Integer, db.ForeignKey('Doctor.id_doctor'), nullable=False)
    id_sucursal = db.Column(db.Integer, db.ForeignKey('Sucursal.id_sucursal'), nullable=False)
    
    doctor = db.relationship('Doctor')
    sucursal = db.relationship('Sucursal')
    
    
class Cita(db.Model):
    __tablename__ = 'Cita'  # nombre exacto de la tabla en tu base de datos

    id_cita = db.Column(db.Integer, primary_key=True)
    fecha_movimiento = db.Column(db.Date, nullable=True)
    finalizada = db.Column(db.Boolean, nullable=True, default=False)
    
    id_paciente = db.Column(db.Integer, db.ForeignKey('Paciente.id_paciente'), nullable=False)
    id_cita_disponible = db.Column(db.Integer, db.ForeignKey('Citas_Disponibles.id_cita_disponibles'), nullable=False)
    
    paciente = db.relationship('Paciente')
    cita_disponible = db.relationship('CitasDisponibles')

class Venta(db.Model):
    __tablename__ = 'Venta'  # nombre exacto de la tabla en tu base de datos

    id_venta = db.Column(db.Integer, primary_key=True)
    fecha_venta = db.Column(db.Date, nullable=True)
    total_venta = db.Column(db.Numeric(10,2), nullable=False)
    
    id_paciente = db.Column(db.Integer, db.ForeignKey('Paciente.id_paciente'), nullable=False)
    id_empleado = db.Column(db.Integer, db.ForeignKey('Empleado.id_empleado'), nullable=False)
    id_pago = db.Column(db.Integer, db.ForeignKey('Formas_de_pago.id_pago'), nullable=False)
    
    pago = db.relationship('FormasDePago')
    paciente = db.relationship('Paciente')
    empleado = db.relationship('Empleado')
    
class Proveedor(db.Model):
    __tablename__ = 'Proveedor'  # nombre exacto de la tabla en tu base de datos
    id_proveedor = db.Column(db.Integer, primary_key=True)
    nombre_proveedor = db.Column(db.String(100), nullable=False)
    calle = db.Column(db.String(100), nullable=False)
    numero_exterior = db.Column(db.String(10), nullable=False)
    numero_interior = db.Column(db.String(10), nullable=True)
    codigo_postal = db.Column(db.String(10), nullable=False)
    nombre_colonia = db.Column(db.String(100), nullable=False)
    numero_telefono = db.Column(db.String(15), nullable=True)
    numero_celular = db.Column(db.String(15), nullable=True)
    correo_electronico = db.Column(db.String(100), nullable=True)
    id_municipio = db.Column(db.Integer, db.ForeignKey('Municipio.id_municipio'), nullable=False)  # Cambias a NOT NULL en MySQL
    id_tipo_colonia = db.Column(db.Integer, db.ForeignKey('Tipos_Colonias.id_tipo_colonia'), nullable=False)  # Cambias a NOT NULL en MySQL
    
    municipio = db.relationship('Municipio')
    tipo_colonia = db.relationship('Tipos_Colonias')

class Producto(db.Model):
    __tablename__ = 'Producto'  # nombre exacto de la tabla en tu base de datos

    id_producto = db.Column(db.Integer, primary_key=True)
    nombre_producto = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text, nullable=False)
    precio = db.Column(db.Numeric(10,2), nullable=False)
    cantidad_disponible = db.Column(db.Integer, nullable=False)
    
    id_proveedor = db.Column(db.Integer, db.ForeignKey('Proveedor.id_proveedor'), nullable=True)
    
    sucursal = db.relationship('Proveedor')
    
class Inventario(db.Model):
    __tablename__ = "Inventario"
    
    id_inventario = db.Column(db.Integer, primary_key=True)
    id_producto = db.Column(db.Integer, db.ForeignKey('Producto.id_producto'), nullable=False)
    id_sucursal = db.Column(db.Integer, db.ForeignKey('Sucursal.id_sucursal'), nullable=False)
    
    producto = db.relationship('Producto')
    sucursal = db.relationship('Sucursal')

class DetalleVenta(db.Model):
    __tablename__ = 'Detalle_Venta'  # nombre exacto de la tabla en tu base de datos

    id_detalle_venta = db.Column(db.Integer, primary_key=True)
    cantidad = db.Column(db.Integer, nullable=False)
    precio_unitario = db.Column(db.Numeric(10,2), nullable=False)
    subtotal = db.Column(db.Numeric(10,2), nullable=False)
    
    def __init__(self, cantidad, precio_unitario):
        self.cantidad = cantidad
        self.precio_unitario = precio_unitario
        self.subtotal = cantidad * precio_unitario
    
    id_venta = db.Column(db.Integer, db.ForeignKey('Venta.id_venta'), nullable=False)
    id_producto = db.Column(db.Integer, db.ForeignKey('Producto.id_producto'), nullable=False)
    
    venta = db.relationship('Venta')
    producto = db.relationship('Producto')

class Usuario(db.Model):
    __tablename__ = 'Usuario'  # nombre exacto de la tabla en tu base de datos

    id_usuario = db.Column(db.Integer, primary_key=True)
    nombre_usuario = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    contrasenia = db.Column(db.String(1000), nullable=False)  # se recomienda guardar hashes
    
    id_rol = db.Column(db.Integer, db.ForeignKey('Rol.id_rol'), nullable=False)
    id_paciente = db.Column(db.Integer, db.ForeignKey('Paciente.id_paciente'), nullable=True)
    id_empleado = db.Column(db.Integer, db.ForeignKey('Empleado.id_empleado'), nullable=True)

    rol = db.relationship('Rol')
    paciente = db.relationship('Paciente')
    empleado = db.relationship('Empleado')
    
# A partir de aqui son las vistas de la base de datos
