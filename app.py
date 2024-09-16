from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)

# Configuración para la carga de archivos
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

# Credenciales de inicio de sesión
USUARIO_VALIDO = "empleado"
CONTRASENA_VALIDO = "$uper4utos#"

# Clase Auto
class Auto:
    def __init__(self, idTipoAuto, marca, modelo, descripcion, precio, cantidad, imagen_url):
        self.idTipoAuto = idTipoAuto
        self.marca = marca
        self.modelo = modelo
        self.descripcion = descripcion
        self.precio = precio
        self.cantidad = cantidad
        self.imagen_url = imagen_url

# Lista para almacenar los autos
autos = []

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/', methods=['GET', 'POST'])
def inicio_sesion():
    if request.method == 'POST':
        usuario = request.form.get('usuario')
        contrasena = request.form.get('contrasena')

        if usuario == USUARIO_VALIDO and contrasena == CONTRASENA_VALIDO:
            return redirect(url_for('registro_auto'))
        else:
            return render_template('inicio.html', error='Credenciales incorrectas.')

    return render_template('inicio.html')

@app.route('/registro_auto', methods=['GET', 'POST'])
def registro_auto():
    if request.method == 'POST':
        idTipoAuto = request.form.get('idTipoAuto')
        marca = request.form.get('marca')
        modelo = request.form.get('modelo')
        descripcion = request.form.get('descripcion')
        precio = request.form.get('precio')
        cantidad = request.form.get('cantidad')
        imagen = request.files.get('imagen')

        # Verificar si el idTipoAuto ya existe
        if any(auto.idTipoAuto == idTipoAuto for auto in autos):
            return render_template('registro_auto.html', mensaje='Error: El ID Tipo de Auto ya existe.')

        # Guardar la imagen si es válida
        imagen_url = ''
        if imagen and allowed_file(imagen.filename):
            filename = f"{idTipoAuto}_{imagen.filename}"
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            imagen.save(filepath)
            imagen_url = url_for('static', filename=f'uploads/{filename}')

        # Agregar el nuevo auto a la lista
        nuevo_auto = Auto(idTipoAuto, marca, modelo, descripcion, precio, cantidad, imagen_url)
        autos.append(nuevo_auto)

        mensaje = "Auto registrado correctamente."
        return render_template('registro_auto.html', mensaje=mensaje, imagen_url=imagen_url)

    return render_template('registro_auto.html')

@app.route('/autos_registrados')
def autos_registrados():
    return render_template('autos_registrados.html', autos=autos)

@app.route('/eliminar_auto/<idTipoAuto>', methods=['POST'])
def eliminar_auto(idTipoAuto):
    global autos
    autos = [auto for auto in autos if auto.idTipoAuto != idTipoAuto]
    return redirect(url_for('autos_registrados'))

if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(debug=True)
