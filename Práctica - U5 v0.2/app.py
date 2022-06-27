from datetime import datetime

from flask import Flask, request, render_template, redirect, url_for

from flask_sqlalchemy import SQLAlchemy

import hashlib

app = Flask(__name__)
app.config.from_pyfile('config.py')

from models import db
from models import Usuario, Receta, Ingrediente

usuario_actual = None

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
    xtiempo = 0
    if(request.method == 'POST'):
        xtiempo = request.form['tiempo']
        return render_template('consultar_tiempo_elaboracion.html')
    else:
        return render_template('consultar_tiempo_elaboracion.html', recetas = Receta.query.order_by(-Receta.cantidadmeusta).all(), bandera = band, tiempo=xtiempo)
@app.route('/consultar_receta_ingrediente')
def consultar_receta_ingrediente():
    pass
if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)