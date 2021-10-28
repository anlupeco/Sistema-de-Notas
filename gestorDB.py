import os
from flask import Flask, request, render_template
from forms import Login
#importar el modulo sqlite3
import sqlite3
#importar modulo de error de sqlite3
from sqlite3 import Error
from flask import current_app, g


#Archivo pensado para colocar las funciones con los quieris, para mejorar visibilidad de codigo

#Conexión con la base de datos
def get_db():
    try:
        if 'db' not in g:
            print('conectada')
            g.db = sqlite3.connect('dataProyecto.db')
        return g.db
    except Error:
        print(Error)


def close_db():
    db = g.pop( 'db', None )

    if db is not None:
        db.close()



# def editar_producto():
#     '''id = request.args.get('id') #captura de la variable id enviada a través de la URL'''
#     codigo = request.args.get('codigo') #captura de la vble código enviada a través de la URL
#     nombre = request.args.get('nombre') #captura de la vble nombre enviada a través de la URL
#     precio = request.args.get('precio') #captura de la vble nombre enviada a través de la URL
#     cantidad = request.args.get('cantidad') #captura de la vble cantidad enviada a través de la URL
#     sql_edit_producto(codigo, nombre, precio, cantidad) #llamado de la función de edición de la base de datos
#     return "OK"

# def borrar_producto():
# 	id = request.args.get('id') #captura de la variable id enviada a través de la URL
# 	sql_delete_producto(id) #llamado a la función de borrado de la base de datos
# 	return "OK"


# '''Rutina SQL para insertar datos en una tabla'''
# def sql_insert_producto(codigo, nombre, precio, cantidad):
#     #crear una variable que contenga la cadena sql que inserta los datos recibidos por parámetro
#     strsql = "insert into producto (id, nombre, precio, existencia) values('"+codigo+"', '"+nombre+"', "+precio+", "+cantidad+");"
#     #el objeto con obtiene la conexión con la base de datos llamando al método creado anteriormente
#     con = sql_connection()
#     #es necesario un objeto cursor, el cual se obtiene de la variable de conexión, para ejecutar las sentencias sql
#     cursorObj = con.cursor()
#     #ejecutar la sentencia sql enviada por parámetro
#     cursorObj.execute(strsql)
#     #actualizar los cambios realizados a la base de datos
#     con.commit()
#     #cerrar la conexión
#     con.close()

# '''Rutina para crear una consulta de todos los datos de una tabla'''
# def sql_select_productos():
#         strsql = "select * from producto;"
#         con = sql_connection()
#         cursorObj = con.cursor()
#         cursorObj.execute(strsql)
#         productos = cursorObj.fetchall()
#         return productos

# '''Rutina para actualizar los datos de una tabla'''
# def sql_edit_producto(codigo, nombre, precio, cantidad):
#         strsql = "update producto set id = '"+codigo+"', nombre = '"+nombre+"', precio = "+precio+", existencia = "+cantidad+" where id = "+codigo+";"
#         con = sql_connection()
#         cursorObj = con.cursor()
#         cursorObj.execute(strsql)
#         con.commit()
#         con.close()

# '''Rutina para borrar los datos de una tabla a traves del ingreso de un codigo referenciado'''
# def sql_delete_producto(id):
#     strsql = "delete from producto where id = "+id+";"
#     con = sql_connection()
#     cursorObj = con.cursor()
#     cursorObj.execute(strsql)
#     con.commit()
#     con.close()