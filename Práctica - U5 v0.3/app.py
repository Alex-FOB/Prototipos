from datetime import datetime

from flask import Flask, request, render_template, redirect, url_for

from flask_sqlalchemy import SQLAlchemy

import hashlib

app = Flask(__name__)
app.config.from_pyfile('config.py')

from models import db
from models import Usuario, Receta, Ingrediente

usuario_actual = None
xtiempo = 0.0
xrecetas = []
xingrediente = 'Ingrediente...'
recetaId = None

@app.route('/', methods = ['GET', 'POST'])
def inicio():
    if(request.method == 'POST'):
        global usuario_actual
        usuario_actual = Usuario.query.filter_by(correo=request.form['correo']).first()
        if usuario_actual is None: #verifica que el correo/usuario esté en la base de datos
            return render_template('error.html', error = 'ERROR: Cuenta no registrada')
        else:
            #verifica que la contraseña ingresada sea igual a la que se encuentra en la base de datos
            #----------------------------------------------------------------------------------------------------------
            resultado = hashlib.md5(bytes(request.form['password'], encoding='utf-8'))
            #----------------------------------------------------------------------------------------------------------
            if(resultado.hexdigest() == usuario_actual.clave): 
                return redirect(url_for('menu'))
            else:
                return render_template('error.html', error = 'ERROR: Contraseña incorrecta')
                #return render_template('menu.html', usuario = usuario_actual)
    else:
        return render_template('ingresar_usuario.html')
@app.route('/menu')
def menu():
    global usuario_actual
    #SETEO DE VARIABLES GLOBALES-----
    global xtiempo
    global xingrediente
    global xrecetas
    global recetaId
    recetaId = None
    xrecetas = []
    xingrediente = 'Ingrediente...'
    xtiempo = 0.0
    #-------------------------------
    return render_template('menu.html', usuario = usuario_actual)
@app.route('/ingresar_receta', methods = ['GET', 'POST'])
def ingresar_receta():
    band = False
    i = 1
    lista = []
    #global usuario_actual  
    if(request.method == 'POST'):
        try:
            #RECETA
            xnombre = str(request.form['nombre']).capitalize()
            xtiempo = float(request.form['tiempo'])
            if(xtiempo <= 0):
                raise ValueError
            nueva_receta = Receta(nombre=xnombre, tiempo=xtiempo, fecha=datetime.now(), elaboracion=request.form['elaboración'], 
                                    cantidadmegusta = 0, usuarioid = request.form['userId'])
            #INGREDIENTE
            idReceta = len(Receta.query.order_by(Receta.id).all())
            while not band and i <= 10:
                inombre = str(request.form['nombre_ingrediente'+str(i)])
                icantidad = request.form['cantidad'+str(i)]
                iunidad = str(request.form['unidad'+str(i)])
                if(inombre != '' and icantidad != '' and iunidad != ''):
                    nuevo_ingrediente = Ingrediente(nombre=inombre, cantidad=icantidad, unidad=iunidad, recetaid=idReceta+1)
                    lista.append(nuevo_ingrediente)
                else:
                    band = True
                i+=1
            #CARGAR LOS DATOS
                #RECETA
            if(len(lista) > 0):
                db.session.add(nueva_receta)
                db.session.commit()
                    #INGREDIENTES
                for ingrediente in lista:
                    db.session.add(ingrediente)
                    db.session.commit()
            elif(len(lista) == 0):
                return render_template('error2.html', error = 'ERROR: no hay ingredientes') 
            return render_template('menu.html')
        except ValueError:
            return render_template('error2.html', error = 'ERROR: valor inválido')             
    else:
        return render_template('nueva_receta.html', usuario = usuario_actual)
@app.route('/consultar_ranking')
def consultar_ranking():
    return render_template('consultar_ranking.html', recetas = Receta.query.order_by(-Receta.cantidadmegusta).limit(5))
@app.route('/consultar_tiempo_elaboracion',  methods = ['GET', 'POST'])
def consultar_tiempo_elaboracion():
    band = False
    global xtiempo
    global xrecetas
    global usuario_actual
    global recetaId
    xanterior = url_for('consultar_tiempo_elaboracion')
    if(request.method == 'POST'):
        xtiempo = request.form['tiempo']
        xrecetas = Receta.query.filter(Receta.tiempo < xtiempo).all()
        if(request.form['aviso'] == 'True'):
            xreceta = Receta.query.filter_by(id=request.form['idReceta']).first()
            xingredientes = xreceta.ingrediente
            recetaId = xreceta.id
            return render_template('receta.html', usuario = usuario_actual,receta = xreceta, anterior = xanterior, ingredientes = xingredientes, band = True)
        return render_template('consultar_tiempo_elaboracion.html', usuario = usuario_actual, recetas = xrecetas, bandera = band, tiempo=xtiempo)
    else:
        xrecetas = Receta.query.filter(Receta.tiempo < xtiempo).all()
        return render_template('consultar_tiempo_elaboracion.html', recetas = xrecetas, bandera = band, tiempo=xtiempo)

def listar(xingrediente): #DEVUELVE UNA LISTA DE RECETAS EN BASE UN INGREDIENTE DE LA MISMA
    lista = []
    recetas = Receta.query.all()
    for receta in recetas:
        i = 0
        band = False
        ingredientes = Ingrediente.query.filter_by(recetaid=receta.id).all()
        while not band and i < len(ingredientes):
            if(xingrediente in str(ingredientes[i].nombre).lower()):
                lista.append(receta)
                band = True
            i+=1
    return lista

@app.route('/consultar_receta_ingrediente', methods = ['GET', 'POST'])
def consultar_receta_ingrediente():
    global usuario_actual
    global xrecetas
    global xingrediente
    global recetaId
    xanterior = url_for('consultar_receta_ingrediente')
    if(request.method == 'POST'):
        if(request.form['aviso'] == 'True'):
            xreceta = Receta.query.filter_by(id=request.form['idReceta']).first()
            xingredientes = xreceta.ingrediente
            recetaId = xreceta.id
            return render_template('receta.html', usuario = usuario_actual,receta = xreceta, anterior = xanterior, ingredientes = xingredientes, band = True)
        xingrediente = str(request.form['ingrediente']).lower()
        xrecetas = listar(xingrediente)
        return render_template('consultar_receta_ingrediente.html', recetas = xrecetas, ingrediente = xingrediente)
    else:
        return render_template('consultar_receta_ingrediente.html', recetas = xrecetas, ingrediente = xingrediente)
@app.route('/receta_datos', methods = ['GET', 'POST']) #MUESTRA LOS DATOS DE UNA RECETA
def receta_datos():
    global usuario_actual
    global recetaId
    xanterior = request.form['anterior']
    if(request.method == 'POST'):
        xreceta = Receta.query.filter_by(id=recetaId).first()
        xingredientes = xreceta.ingrediente
        xreceta.cantidadmegusta += 1
        db.session.commit()
        return render_template('receta.html', usuario = usuario_actual, receta = xreceta, anterior = xanterior, ingredientes = xingredientes, band = False)
if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)