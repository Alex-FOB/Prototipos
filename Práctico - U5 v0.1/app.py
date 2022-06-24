from datetime import datetime

from flask import Flask, request, render_template

from flask_sqlalchemy import SQLAlchemy

import hashlib

app = Flask(__name__)
app.config.from_pyfile('config.py')

from models import db
from models import Usuario, Receta, Ingrediente

@app.route('/', methods = ['GET', 'POST'])
def inicio():
    if(request.method == 'POST'):
        if(not request.form['correo'] or not request.form['password']): #verifica que se haya ingresado datos en el formulario
            return render_template('error.html', error = 'ERROR: Faltan datos')
        else:
            usuario_actual = Usuario.query.filter_by(correo = request.form['correo']).first()
            if usuario_actual is None: #verifica que el correo/usuario esté en la base de datos
                return render_template('error.html', error = 'ERROR: Cuenta no registrada')
            else:
                #verifica que la contraseña ingresada sea igual a la que se encuentra en la base de datos
                #----------------------------------------------------------------------------------------------------------
                resultado = hashlib.md5(bytes(request.form['password'], encoding='utf-8'))
                #----------------------------------------------------------------------------------------------------------
                if(resultado.hexdigest() == usuario_actual.clave): 
                    return render_template('menu.html', usuario = usuario_actual)
                else:
                    return render_template('error.html', error = 'ERROR: Contraseña incorrecta')
                    #return render_template('menu.html', usuario = usuario_actual)
    else:
        return render_template('ingresar_usuario.html')
@app.route('/ingresar_receta')
def ingresar_receta():
    pass
@app.route('/consultar_ranking')
def consultar_ranking():
    pass
@app.route('/consultar_tiempo_elaboracion')
def consultar_tiempo_elaboracion():
    pass
@app.route('/consultar_receta_ingrediente')
def consultar_receta_ingrediente():
    pass
def menu():
    pass
if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)