# app.py
from flask import Flask, render_template, redirect, url_for
from flask_login import LoginManager, login_user, login_required
from flask_sqlalchemy import SQLAlchemy

from conexion.conexion import crear_conexion

app = Flask(__name__)
app.config['SECRET_KEY'] = 'tu_clave_secreta'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/usuarios.db'
app.config['SQLALCHEMY_BINDS'] = {
    'mysql': 'mysql+mysqlconnector://root:@localhost/desarrollo_web'
}

# Configuración de Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Configuración de bases de datos
db = SQLAlchemy(app)

# Importar blueprints y modelos después de inicializar db
from models.user import User
from forms import login, ProductForm

# Rutas principales
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/usuario/<nombre>')
def usuario(nombre):
    return f'Bienvenido, {nombre}!'

# ... (resto de rutas para formularios, CRUD, etc.)

if __name__ == '__main__':
    app.run(debug=True)


    # En app.py
    @app.route('/productos')
    @login_required
    def productos():
        conexion = crear_conexion()
        cursor = conexion.cursor(dictionary=True)
        cursor.execute("SELECT * FROM productos")
        productos = cursor.fetchall()
        cursor.close()
        conexion.close()
        return render_template('productos.html', productos=productos)


    @app.route('/crear', methods=['GET', 'POST'])
    @login_required
    def crear_producto():
        form = ProductForm
        if form.validate_on_submit():
            # Guardar en MySQL
            conexion = crear_conexion()
            cursor = conexion.cursor()
            cursor.execute("INSERT INTO productos (nombre, precio, stock) VALUES (%s, %s, %s)",
                           (form.nombre.data, form.precio.data, form.stock.data))
            conexion.commit()
            cursor.close()
            conexion.close()
            return redirect(url_for('productos'))
        return render_template('formulario.html', form=form)


    # En app.py
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))


    @app.route('/login', methods=['GET', 'POST'])
    def login():
        form = login()
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user and user.password == form.password.data:
                login_user(user)
                return redirect(url_for('index'))
        return render_template('login.html', form=form)