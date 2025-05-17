from flask import *
from werkzeug.security import generate_password_hash, check_password_hash
from entities import *
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature
from datetime import datetime

serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])

@app.route('/')
def index():
    """
    Esta función maneja la ruta raíz de la aplicación y redirige a la página de inicio de sesión.

    Returns:
        template (str): index.html
    """
    return render_template('index.html')
    
@app.route('/farmacia-alejo/home', methods=['GET', 'POST'])
def pagina_principal():
    
    """
    Esta función maneja la ruta de la página principal de la aplicación.
    Si el método de la solicitud es POST, se procesa el formulario de inicio de sesión.
    Si el método es GET, se verifica el token de sesión y se muestra la página principal.
    Si el token es válido, se muestra la página principal con el nombre de usuario y tipo de usuario.
    Si el token es inválido o ha expirado, se redirige al usuario a la página de inicio de sesión con un mensaje de error.
    Returns:
        Respomse: redirect(url_for('login'))
        template (str): pagina_principal.html
    """

    token = request.args.get('token')
    usuario = request.args.get('usuario')

    try:
        usuario_token = serializer.loads(token, salt='token-salt', max_age=3600)

        if usuario_token != session.get('token'):
            flash('Token no válido para este usuario.', 'error')
            return redirect(url_for('login'))

        # Puedes guardar información en session si deseas mantener sesión activa
        session['nombre_usuario'] = usuario

        return render_template(
            'pagina_principal.html',
            nombre_usuario=session.get('nombre_usuario'),
            tipo_usuario=session.get('tipo_usuario')
        )

    except SignatureExpired:
        flash('El token ha expirado. Por favor, vuelve a iniciar sesión.', 'error')
        return redirect(url_for('login'))

    except BadSignature:
        flash('Token inválido.', 'error')
        return redirect(url_for('login'))

@app.route('/farmacia-alejo/forgot-password', methods=['GET', 'POST'])
def forgot_password():

    """
    Esta función maneja la ruta de recuperación de contraseña.
    Si el método de la solicitud es POST, se procesa el formulario de recuperación de contraseña.
    Si el método es GET, se muestra la página de recuperación de contraseña.
    Returns:
        Response: redirect(url_for('login'))
        template (str): forgot_password.html
    """
    pass

@app.route('/farmacia-alejo/register', methods=['GET', 'POST'])
def register():

    """
    Esta función maneja la ruta de registro de nuevos usuarios.
    Si el método de la solicitud es POST, se procesa el formulario de registro.
    Se verifica si el nombre de usuario y el correo electrónico ya existen en la base de datos.
    Si las contraseñas coinciden, se crea un nuevo usuario y se redirige a la página de inicio de sesión.
    Si el método es GET, se muestra la página de registro.
    Args:
        request (Request): La solicitud HTTP que contiene los datos del formulario de registro.

    Returns:
        Response: redirect(url_for('login'))
        template (str): register.html
        Response: redirect(url_for('register'))
    """
    
    
    if request.method == 'POST':
        tipo_usuario = 'Usuario'
        username = request.form['nombre_usuario']
        primer_nombre = request.form['nombre']
        segundo_nombre = request.form['segundo_nombre']
        primer_apellido = request.form['apellido']
        segundo_apellido = request.form['segundo_apellido']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        # Aqui se obtiene el registro del rol de Paciente
        rol = Rol.query.filter_by(tipo_rol=tipo_usuario).first()
        if not rol:
            flash("Rol no válido.")
            return redirect(url_for('register'))
        
        # Verifica si el nombre de usuario ya existe
        usuario_existente = Usuario.query.filter_by(nombre_usuario=username).first()
        if usuario_existente:
            flash("El nombre de usuario ya está en uso. Elige otro.")
            return redirect(url_for('register'))

        # Verifica si el usuario ya existe
        if Usuario.query.filter_by(email=email).first():
            flash('El correo ya está registrado')
            return redirect(url_for('login'))

        # Verifica si las contraseñas coinciden
        if password != confirm_password:
            flash("Las contraseñas no coinciden.")
            return redirect(url_for('register'))

        # Se crea el registro del nuevo paciente en el sistema (Simulando un trigger)
        nuevo_paciente = Paciente(nombre=primer_nombre, segundo_nombre=segundo_nombre, apellido=primer_apellido, segundo_apellido=segundo_apellido, edad=None, direccion=None)
        db.session.add(nuevo_paciente)
        db.session.commit()

        # Crea un nuevo usuario
        nuevo_usuario = Usuario(nombre_usuario=username ,email=email, contrasenia=generate_password_hash(password), id_empleado=None, id_paciente=nuevo_paciente.id_paciente, id_rol=rol.id_rol)
        db.session.add(nuevo_usuario)
        db.session.commit()
        

        flash('Usuario registrado exitosamente')
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/farmacia-alejo/login', methods=['GET', 'POST'])
def login():
    
    """
    Esta función maneja la ruta de inicio de sesión.
    Si el método de la solicitud es POST, se procesa el formulario de inicio de sesión.
    Se verifica si el correo electrónico y la contraseña son correctos.
    Si son correctos, se genera un token y se redirige a la página principal.
    Si no son correctos, se muestra un mensaje de error.
    Si el método es GET, se muestra la página de inicio de sesión.
    Args:
        request (Request): La solicitud HTTP que contiene los datos del formulario de inicio de sesión.
        session (Session): La sesión del usuario actual.
        serializer (URLSafeTimedSerializer): El serializador para generar y verificar tokens.
        Usuario (Model): El modelo de usuario de la base de datos.
        check_password_hash (function): Función para verificar la contraseña hasheada.
        flash (function): Función para mostrar mensajes flash al usuario.
        redirect (function): Función para redirigir a otra ruta.
        url_for (function): Función para generar URLs para las rutas de la aplicación.
        render_template (function): Función para renderizar plantillas HTML.

    Returns:
        Response: redirect(url_for('pagina_principal'))
        template (str): index.html
        Response: redirect(url_for('login'))
    """
    
    
    if request.method == 'POST':
        tipo_usuario = request.form['opcion']
        email = request.form['email']
        password_ingresada = request.form['password']

        usuario = Usuario.query.filter_by(email=email).first()
        
        if not usuario:
            flash('El correo no está registrado', 'error')
            return redirect(url_for('login'))
        
        if tipo_usuario == 'Seleccione':
            flash('Debe seleccionar el tipo de usuario', 'error')
            return redirect(url_for('login'))

        if usuario and check_password_hash(usuario.contrasenia, password_ingresada):
            tipo_usuario_bd = usuario.rol.tipo_rol if usuario.rol else 'Desconocido'

            if tipo_usuario != tipo_usuario_bd:
                flash('Tipo de usuario incorrecto para este correo', 'error')
                return redirect(url_for('login'))
            
            token_random = secrets.token_urlsafe(32)

            token_final = serializer.dumps(token_random, salt='token-salt')

            session['id_usuario'] = usuario.id_usuario
            session['nombre_usuario'] = usuario.nombre_usuario
            session['tipo_usuario'] = tipo_usuario_bd
            session['email'] = usuario.email
            session['token'] = token_random

            return redirect(url_for('pagina_principal', usuario=usuario.nombre_usuario, token=token_final))
        elif not usuario or not check_password_hash(usuario.contrasenia, password_ingresada):
            flash('Correo o contraseña incorrectos', 'error')
            return redirect(url_for('login'))
        else:
            flash('Error al iniciar sesión', 'error')
            return redirect(url_for('login'))

    return render_template('index.html')


@app.route('/farmacia-alejo/citas', methods=['GET', 'POST'])
def citas():
    """
    Esta función maneja la ruta de agendar citas.
    Si el método de la solicitud es POST, se procesa el formulario de agendar cita.
    Se verifica si la cita ya está reservada y se crea una nueva cita en la base de datos.
    Si el método es GET, se muestra la lista de citas disponibles.
    Args:
        request (Request): La solicitud HTTP que contiene los datos del formulario de agendar cita.
        session (Session): La sesión del usuario actual.
        CitasDisponibles (Model): El modelo de citas disponibles de la base de datos.
        Paciente (Model): El modelo de paciente de la base de datos.
        Cita (Model): El modelo de cita de la base de datos.
        db (SQLAlchemy): La instancia de SQLAlchemy para interactuar con la base de datos.
        flash (function): Función para mostrar mensajes flash al usuario.
        redirect (function): Función para redirigir a otra ruta.
        url_for (function): Función para generar URLs para las rutas de la aplicación.
        render_template (function): Función para renderizar plantillas HTML.
        datetime (module): Módulo para trabajar con fechas y horas.

    Returns:
        Response: redirect(url_for('pagina_principal'))
        template (str): agendar.html
    """

    if request.method == 'POST':
        cita_id = request.form['cita_id']
        
        consulta = CitasDisponibles.query.filter_by(id_cita=cita_id).first()
        paciente = Paciente.query.filter_by(id_paciente=session['id_usuario']).first()

        # Falta agregar la lógica para evitar citas empalmadas
        cita_paciente = Cita.query.filter_by(id_paciente=paciente.id_paciente, id_cita=consulta.id_cita).first()
        
        consulta.disponible = False
        db.session.commit()

        nueva_cita = Cita(paciente.id_paciente, consulta.id_cita, fecha_movimiento=datetime.now(), finalizada=False)
        db.session.add(nueva_cita)
        db.session.commit()
        
        flash('Cita reservada exitosamente', 'success')
        return redirect(url_for('pagina_principal', usuario=session['nombre_usuario'], token=session['token']))

    citas = CitasDisponibles.query.all()
    return render_template('agendar.html', citas=citas)

@app.route('/logout')
def logout():
    
    """
    Esta función maneja la ruta de cierre de sesión.
    Elimina los datos de la sesión y redirige al usuario a la página de inicio de sesión.
    Args:
        session (Session): La sesión del usuario actual.
        flash (function): Función para mostrar mensajes flash al usuario.
        redirect (function): Función para redirigir a otra ruta.
        url_for (function): Función para generar URLs para las rutas de la aplicación.
    Returns:
        Response: redirect(url_for('login'))
    """
    
    # Eliminar los datos de la sesión
    session.pop('id_usuario', None)
    session.pop('nombre_usuario', None)
    session.pop('tipo_usuario', None)
    session.pop('email', None)
    session.pop('token', None)

    # Flash para informar al usuario que ha cerrado sesión
    flash('Has cerrado sesión exitosamente.', 'success')

    # Redirigir al usuario a la página de inicio de sesión
    return redirect(url_for('login'))

def pagina_no_encontrada(e):
    
    """
    Esta función maneja la ruta de error 404 (Página no encontrada).
    Se muestra una página personalizada de error 404.
    Args:
        e (Exception): La excepción que se ha producido.
        render_template (function): Función para renderizar plantillas HTML.
        Response: La respuesta HTTP que se enviará al cliente.
    Returns:
        Response: render_template('404.html'), 404
    """
    
    return render_template('404.html'), 404

if __name__ == "__main__":
    
    """
    Esta función se ejecuta al iniciar la aplicación.
    Se registra un manejador de errores para el error 404 (Página no encontrada).
    Se inicia el servidor Flask en modo de depuración en el puerto 5000.

    Args:
        app (Flask): La instancia de la aplicación Flask.
        db (SQLAlchemy): La instancia de SQLAlchemy para interactuar con la base de datos.
        SystemExit (Exception): Excepción que se produce al salir del programa.
        RuntimeError (Exception): Excepción que se produce en tiempo de ejecución.
    """

    app.register_error_handler(404, pagina_no_encontrada)
    
    try:
        app.run(debug = True, port = 5000)
        db.session.close()
        db.engine.dispose()
    except SystemExit as e:
        print("Error al iniciar el servidor:", e.code)
    except RuntimeError as e:
        print("Error de tiempo de ejecución:", e)
    finally:
        print("Conexión a la base de datos cerrada.")