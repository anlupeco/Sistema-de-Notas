from flask import Flask, render_template, flash, request, redirect, url_for, session, send_file, current_app, g, make_response
from flask import render_template as render
from flask import redirect
from sqlite3 import Error
from werkzeug.security import generate_password_hash, check_password_hash

import functools
import os
from re import X

from forms import Login
import gestorDB 
import utils

app = Flask(__name__)
app.secret_key = os.urandom(24)

sesion_iniciada = False;

@app.route("/", methods=['GET', 'POST'])
def inicio():
    if g.userEstudiante:
        return redirect( url_for( 'homeEstudiante' ) )
    if g.userProfesor:
        return redirect( url_for( 'homeProfesor' ) )
    if g.userAdmin:
        return redirect( url_for( 'dashboard' ) )
    #Pagina index para inciar sesión
    return render("index.html")

#login - conexión base de datos 
@app.route('/login', methods=['GET', 'POST'])
def login():
    try:
        if g.userEstudiante:
            return redirect( url_for( 'homeEstudiante' ) )
        if g.userProfesor:
            return redirect( url_for( 'homeProfesor' ) )
        if g.userAdmin:
            return redirect( url_for( 'dashboard' ) )

        if request.method == 'POST':
            db = gestorDB.get_db()
            error = None
            username = request.form['codigo']
            password = request.form['password']
            rol = request.form['rol']
            

            if not username:
                error = 'Debes ingresar el usuario'
                flash( error )
                return render_template( 'index.html' )

            if not password:
                error = 'Contraseña requerida'
                flash( error )
                return render_template( 'index.html' )
            
            NombreRol=""
            session['rol'] = rol
            if rol =="1":
                NombreRol='estudiante'
            elif rol =="2":
                NombreRol ='profesor'
            else:
                NombreRol='administrador'

            user = db.execute(
                'SELECT * FROM '+NombreRol+' WHERE  codigo = ? AND password = ? ', (username, password)
            ).fetchone()

            if user is None:
                user = db.execute(
                    'SELECT * FROM '+NombreRol+' WHERE codigo = ?', (username,)
                ).fetchone()
                if user is None:
                    error = 'Usuario no existe'
                else:
                    #Validar contraseña hash            
                    store_password = user[2]
                    result = check_password_hash(store_password, password)
                    if result is False:
                        error = 'Contraseña inválida'
                    else:
                        if (rol==1):
                            session.clear()
                            session['user_id1'] = user[1]
                            resp = make_response( redirect( url_for( 'homeEstudiante' ) ) )
                            resp.set_cookie( 'username', username )
                            return resp
                        
                        if (rol==2):
                            session.clear()
                            session['user_id2'] = user[1]
                            resp = make_response( redirect( url_for( 'homeProfesor' ) ) )
                            resp.set_cookie( 'username', username )
                            return resp

                                                
                        if (rol==3):
                            session.clear()
                            session['user_id3'] = user[1]
                            resp = make_response( redirect( url_for( 'dashboard' ) ) )
                            resp.set_cookie( 'username', username )
                            return resp

                    flash( error )
            
            else:
                if rol == "1":
                    home='homeEstudiante'
                    session.clear()
                    session['user_id1'] = user[1]
                    return redirect( home)                    
                if rol == "2":
                    home ='homeProfesor'
                    session.clear()
                    session['user_id2'] = user[1]
                    return redirect( home)
                if rol== "3":
                    home='dashboard'
                    session.clear()
                    session['user_id3'] = user[1]
                    return redirect( home)
                
            flash( error )
            gestorDB.close_db()
                


            flash( error )
        return render_template( 'index.html' )
    except:
        return render_template( 'index.html' )

@app.route('/recordarPass', methods=['GET'])
def recordar_pass():
    return render("recordarPass.html")




@app.route('/dashboard/<rol_usuario>', methods=['GET', 'POST'])
def usuario(rol_usuario):
    if rol_usuario == "estudiante":
        return render("homeEstudiante.html")
    elif rol_usuario == "profesor":
        return render("homeProfesor.html")
    elif rol_usuario == "admin":
        return render("dashboard.html")


def login_required1(view):
    @functools.wraps( view )
    def wrapped_view(**kwargs):

        # if g.user1 is None:
        #     return redirect( url_for( 'login' ) )
        
        if g.userEstudiante is None:
            return render_template( 'index.html' )

        return view( **kwargs )

    return wrapped_view

def login_required2(view):
    @functools.wraps( view )
    def wrapped_view(**kwargs):

        # if g.user1 is None:
        #     return redirect( url_for( 'login' ) )
        
        if g.userProfesor is None:
            return render_template( 'index.html' )

        return view( **kwargs )

    return wrapped_view

def login_required3(view):
    @functools.wraps( view )
    def wrapped_view(**kwargs):

        # if g.user1 is None:
        #     return redirect( url_for( 'login' ) )
        
        if g.userAdmin is None:
            return render_template( 'Permisos.html' )

        return view( **kwargs )

    return wrapped_view

#----Buscar cursos----------------------------------------------------------------------------------
@app.route('/BuscarCursosAdministrador')
def productos():
  productos = sql_select_productos()
  return render_template('BuscarCursosAdministrador.html', productos = productos)

def sql_select_productos():
        num = 58
        strsql = "select Id,codigo,nombre,asignatura,maxEstudiante,profesor from curso ;"
       # 'SELECT id FROM usuario WHERE correo = ?', (email)
        con = gestorDB.get_db()
        cursorObj = con.cursor()
        cursorObj.execute(strsql)
        productos = cursorObj.fetchall()
        return productos

#----------------------------------------------------------------------------------

#ADMINISTRAD0R----------------------------------------------------------------------------------------------
@app.route("/dashboard", methods=['GET', 'POST'])
@login_required3
def dashboard():
    return render("dashboard.html")

@app.route('/registro', methods=['GET', 'POST'])
@login_required3
def registro():
    return render("registro.html")

@app.route("/BuscarCursosAdministrador", methods=['GET', 'POST'])
@login_required3
def BuscarCursosAdministrador():
    return render("BuscarCursosAdministrador.html")


@app.route("/BuscarUsuarioAdministrador", methods=['GET', 'POST'])
@login_required3
def BuscarUsuarioAdministrador():
    return render("BuscarUsuario.html")


@app.route("/BuscarAsignaturaAdministrador", methods=['GET', 'POST'])
@login_required3
def BuscarAsignaturaAdministrador():
    return render("BuscarAsignaturasAdministrador.html")


@app.route("/crearCursos", methods=['GET', 'POST'])
@login_required3
def crearCursos():
    return render("crearCursos.html")


@app.route("/crearAsignatura", methods=['GET', 'POST'])
@login_required3
def crearAsignatura():
    return render("crearAsignatura.html")


@app.route("/informacionAdministrador", methods=['GET', 'POST'])
@login_required3
def informacionAdministrador():
    return render("informacionAdministrador.html")

#Integración de registro de usuarios 
@app.route( '/registar', methods=('GET', 'POST') )
@login_required3
def registar():
    try:
        if request.method == 'POST':
            print('ENTRA')
            codigo = request.form['codigo']
            name = request.form['name']
            apellido = request.form['apellido']
            tipoDocumento=request.form['tipoDocumento']
            documento = request.form['num_doc']
            password = request.form['password']
            email = request.form['mail']
            fechaNacimiento= request.form['fecha_nac']
            tipoUsuario = request.form['TipoUsuario']

            error = None
            db = gestorDB.get_db()

            # if not name:
            #     error = 'Debes ingresar el nombre del usuario'
            #     flash( error )
            #     return render_template( 'registro.html' )
            
            # if not apellido:
            #     error = 'Debes ingresar el nombre del usuario'
            #     flash( error )
            #     return render_template( 'registro.html' )

            # if not utils.isPasswordValid( password ):
            #     error = 'La contraseña debe contenir al menos una minúscula, una mayúscula, un número y 8 caracteres'
            #     flash( error )
            #     print(error)
            #     return render_template( 'registro.html' )

            # if not utils.isEmailValid( email ):
            #     error = 'Correo invalido'
            #     flash( error )
            #     print(error)
            #     return render_template( 'registro.html' )

            NombreRol=""
            if tipoUsuario =="1":
                NombreRol='estudiante'
            elif tipoUsuario =="2":
                NombreRol ='profesor'
            else:
                NombreRol='administrador'


            print(error)
            print("ENTRAAA")
            
            db.execute('INSERT INTO  '+NombreRol+'     (codigo, password,tipoDeDocumento, cedula,nombres, apellidos, email, fechaDeNacimiento)VALUES(?,?,?,?,?,?,?,?) ', (codigo,generate_password_hash(password),tipoDocumento,documento,name,apellido,email,fechaNacimiento))
            db.commit()

            flash( 'Usuario creado' )
            return render_template( 'registro.html' )
        return render_template( 'registro.html' )
    except:
        return render_template( 'registro.html' )
#Fin de creacion de usuarios 

#Integración de la creación de asignatura
@app.route( '/registro_asignatura', methods=('GET', 'POST') )
@login_required3
def registro_asignatura():
    try:
        if request.method == 'POST':
            print('ENTRA')
            name = request.form['nombre_asignatura']
            codigo = request.form['CodigoAsignatura']
            creditos = request.form['NumeroCreditos']
            maxEstudiante = request.form['MaxEstudiante']
            detalle= request.form['DetalleAsignatura']

            error = None
            db = gestorDB.get_db()
            if not utils.isUsernameValid(name):
                error = "El nombre debe ser alfanumerico o incluir solo '.','_','-'"
                flash( error )
                return render_template( 'crearAsignatura.html' )

            
            if not detalle:
                error = 'Debes ingresar una descripción'
                flash( error )
                return render_template( 'crearAsignatura.html' )


            # if db.execute( 'SELECT codigo FROM asignatura WHERE codigo = ?', (codigo) ).fetchone() is not None:
            #     error = 'El codigo ya existe'.format( codigo )
            #     flash( error )

                return render_template( 'auth/crearAsignatura.html' )
            print(error)
            strsql = "insert into asignatura (codigo, nombre, creditos,detalle) values("+codigo+", '"+name+"', "+creditos+", '"+detalle+"' )"
            db.execute(strsql)
            db.commit()

            flash( 'Asignatura creada' )
            return render_template( 'crearAsignatura.html' )
        return render_template( 'crearAsignatura.html' )
    except:
        return render_template( 'crearAsignatura.html' )
#Fin de creacion de ruta del formulario de creación de asignaturas

#Creacion de cursos 
@app.route( '/registro_curso', methods=('GET', 'POST') )
@login_required3
def registro_curso():
    try:
        if request.method == 'POST':
            print('ENTRA')
            name = request.form['nombreCurso']
            codigo = request.form['CodigoCurso']
            profesorAsociado = request.form['ProfesorCurso']
            maxEstudiante = request.form['MaxEstudiante'] 
            asignatura = request.form['AsignaturaAsociada']

            error = None
            db = gestorDB.get_db()
            if not utils.isUsernameValid(name):
                error = "El nombre debe ser alfanumerico o incluir solo '.','_','-'"
                flash( error )
                return render_template( 'crearCursos.html' )


            # if db.execute( 'SELECT codigo FROM asignatura WHERE codigo = ?', (codigo) ).fetchone() is not None:
            #     error = 'El codigo ya existe'.format( codigo )
            #     flash( error )

             #   return render_template( 'auth/crearAsignatura.html' )
            #print(error)
            strsql = "insert into curso (codigo, nombre, asignatura,maxEstudiante,profesor) values("+codigo+", '"+name+"', '"+asignatura+"',"+maxEstudiante+", '"+profesorAsociado+"' )"
            db.execute(strsql)
            db.commit()

            flash( 'Curso creada' )
            return render_template( 'crearCursos.html' )
        return render_template( 'crearCursos.html' )
    except:
        return render_template( 'crearCursos.html' )
#Fin de creacion de ruta de creacion de curso

#PAGINAS DE PROFESOR-------------------------------------------------------------------------------------

@app.route("/homeProfesor", methods=['GET', 'POST'])
@login_required2
def homeProfesor():
    return render("homeProfesor.html")

@app.route("/misCursosProfesor", methods=['GET', 'POST'])
@login_required2
def misCursosProfesor():
    return render("misCursosProfesor.html")

@app.route("/informacionProfesor", methods=['GET', 'POST'])
@login_required2
def informacionProfesor():
    return render("informacionProfesor.html")

@app.route("/cursoProfesor", methods=['GET', 'POST'])
@login_required2
def cursoProfesor():
    return render("cursoProfesor.html")

@app.route("/detalleActividadProfesor", methods=['GET', 'POST'])
@login_required2
def detalleActividadProfesor():
    return render("detalleActividadProfesor.html")

#PAGINAS DE Estudiante----------------------------------------------------------------------------------

@app.route("/homeEstudiante", methods=['GET', 'POST'])
@login_required1
def homeEstudiante():
    return render("homeEstudiante.html")

@app.route("/registroAsignatura", methods=['GET', 'POST'])
@login_required1
def registroAsignatura():
    return render("registroAsignatura.html")

@app.route("/verNotasEstudiante", methods=['GET', 'POST'])
@login_required1
def verNotasEstudiante():
    return render("verNotasEstudiante.html")

@app.route("/informacionEstudiante", methods=['GET', 'POST'])
@login_required1
def informacionEstudiante():
    return render("informacionEstudiante.html")

@app.route("/cursoEstudiante", methods=['GET', 'POST'])
@login_required1
def cursoEstudiante():
    return render("cursoEstudiante.html")

@app.route("/detalleActividadEstudiante", methods=['GET', 'POST'])
@login_required1
def detalleActividadEstudiante():
    return render("detalleActividadEstudiante.html")

@app.route("/retroalimentacionEstudiante", methods=['GET', 'POST'])
@login_required1
def dretroalimentacionEstudiante():
    return render("retroalimentacionEstudiante.html")

#----------------------------------------------------------------------------------------------------------



@app.route('/perfil', methods=['GET'])
def perfil():
    return render("dashboard.html")



@app.route('/editar', methods=['GET', 'POST'])
def editar():
    return render("informacionEstudiante.html")

@app.route('/MisCursos', methods=['GET'])
def cursos(id_usuario):
    return f"Pagina mis cursos del usuario: {id_usuario}"

@app.route('/verActividades', methods=['GET', 'POST'])
def Actividades():
    return "Pagina para crear/ver actividades de los cursos de acuerdo al rol"

@app.route('/Notas', methods=['GET', 'POST'])
def notas():
    return "Página para ver/asignar notas de acuerdo al rol"

@app.route('/calificaciones', methods=['GET', 'POST'])
def calificaciones():
    return "Pagina para registrar/ver califiacaiones finales de las asignaturas"

@app.route('/detalle', methods=['GET'])
def detalle():
    return "Pagina para ver detalle de actividades y retroalimentacion de notas"

@app.before_request
def load_logged_in_user1():
        user_id = session.get( 'user_id1' )
        
        if user_id is None:
            g.userEstudiante = None
        else:
            g.userEstudiante = gestorDB.get_db().execute(
                'SELECT * FROM estudiante WHERE codigo = ?', (user_id,)
            ).fetchone()

@app.before_request
def load_logged_in_user2():
        user_id = session.get( 'user_id2' )
        
        if user_id is None:
            g.userProfesor = None
        else:
            g.userProfesor = gestorDB.get_db().execute(
                'SELECT * FROM profesor WHERE codigo = ?', (user_id,)
            ).fetchone()

@app.before_request
def load_logged_in_user3():
        user_id = session.get( 'user_id3' )
        
        if user_id is None:
            g.userAdmin = None
        else:
            g.userAdmin = gestorDB.get_db().execute(
                'SELECT * FROM administrador WHERE codigo = ?', (user_id,)
            ).fetchone()


@app.route( '/logout')
def logout():
    session.clear()
    return redirect( url_for( 'login' ) )

if __name__ == "__main__":
    app.run(debug=True);

#---------Seccion para los roles-----------







