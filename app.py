from flask import Flask, request, make_response, redirect, render_template, session, url_for, flash
from flask_bootstrap import Bootstrap


import pdfkit
from flask_sqlalchemy import SQLAlchemy

import mysql.connector
from flask_mysqldb import MySQL,MySQLdb
import bcrypt
app = Flask(__name__)





# Mysql Connection
app.config['MYSQL_HOST'] = 'us-cdbr-east-02.cleardb.com' 
app.config['MYSQL_USER'] = 'b4a513e32e9681'
app.config['MYSQL_PASSWORD'] = '667ca586'
app.config['MYSQL_DB'] = 'heroku_76088dfc864cda7'

mysql = MySQL(app)

# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///DataBase.db"

# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///DataBase.db"

# db = SQLAlchemy(app) 
# login_manager = LoginManager()
# login_manager.init_app(app)
# login_manager.login_view = 'hello'


bootstrap = Bootstrap(app)


app.config['SECRET_KEY'] = 'SUPER SECRETO'

# class User(UserMixin, db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(15), unique=True)
#     email = db.Column(db.String(50), unique=True)
#     password = db.Column(db.String(80))


# @login_manager.user_loader
# def load_user(user_id):
#     return User.query.get(int(user_id))



# class LoginForm(FlaskForm):
#     username = StringField('Nombre de usuario', validators=[DataRequired(),Length(min=4, max=15)])
#     password = PasswordField('Password', validators=[DataRequired(),Length(min=4, max=10)])
#     remember = BooleanField('remember me')

#     submit = SubmitField('Enviar')



# class RegisterForm(FlaskForm):
#     email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
#     username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
#     password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])




@app.errorhandler(404)
def not_found(error):
    return render_template('404.html', error=error)



@app.route('/',methods=['GET'])
def index():
    

    #response = make_response(redirect('/login'))
     return render_template("cartillas.html")
    

    #return response

@app.route('/informacion.html')
def informacionJuego():

     return render_template("informacion.html")
    




@app.route('/static/cargaMasiva.html')

def cargaMasiva():
    return render_template('cargaMasiva.html')



@app.route('/static/cartillas.html')
def cartillas():

    return render_template('cartillas.html')




@app.route('/perfil', methods=['GET'])
def perfil():

    cur = mysql.connection.cursor()
    id = session['id']
    cur.execute('SELECT * FROM users WHERE id = %s',[id])
    data = cur.fetchall()
    cur.close()
    return render_template('perfil.html', users = data)



@app.route('/ActualizarPerfil', methods=['POST'])
def ActualizarPerfil():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE users
            SET name = %s,
                email = %s,
                password = %s
            WHERE id = %s
        """, (name, email, password, session['id']))
        flash('Ussuario actualizado con extito')
        mysql.connection.commit()
        return redirect(url_for('perfil'))





@app.route('/static/Reportes-juegos.html')

def reportes_juegos():
  
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM juegos')
    data = cur.fetchall()
    cur.close()
    return render_template('Reportes-juegos.html', juegos = data)



@app.route('/static/Reportes-usuarios.html')


def reportes_usuarios():
  
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM users')
    data = cur.fetchall()
    cur.close()
    return render_template('Reportes-usuarios.html', users = data)




#Creando el Crud de usuarios

@app.route('/static/Crud_user.html')
def Crud_user():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM users')
    data = cur.fetchall()
    cur.close()
    return render_template('Crud_user.html', users = data)


@app.route('/edit/<id>', methods = ['POST', 'GET'])
def get_user(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM users WHERE id = %s', [id])
    data = cur.fetchall()
    cur.close()
    print(data[0])
    return render_template('edit-users.html', users = data[0])


@app.route('/delete/<string:id>', methods = ['POST','GET'])
def delete_contact(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM users WHERE id = {0}'.format(id))
    mysql.connection.commit()
    flash('Contact Removed Successfully')
    return render_template('Crud_user.html')

@app.route('/update/<id>', methods=['POST'])
def update_contact(id):
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE users
            SET name = %s,
                email = %s,
                password = %s
            WHERE id = %s
        """, (name, email, password, id))
        flash('Ussuario actualizado con extito')
        mysql.connection.commit()
        return render_template('Crud_user.html')






#Metodo para regitrar e ingresar usuarios
@app.route('/validarLogin', methods=['GET', 'POST'])
def validarLogin():
    if request.method == 'POST':
        email = request.form['email']
        #password = request.form['password'].encode('utf-8')
        password = request.form['password']

        curl = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        curl.execute("SELECT * FROM users WHERE email=%s",(email,))
        user = curl.fetchone()
        curl.close()

        if len(user) > 0:
            #if bcrypt.hashpw(password, user["password"].encode('utf-8')) == user["password"].encode('utf-8'):
            if password == user["password"]:
                session['name'] = user['name']
                session['email'] = user['email']
                session['rol'] = user['rol']
                session['id'] = user['id']

                return render_template("cartillas.html")
            else:
                return "Error password and email not match"
        else:
            return "Error user not found"
    else:
        return render_template("cartillas.html")
    
     

    


@app.route('/login')
def irLogin():
    return render_template('Login.html')

    


@app.route('/register', methods=['POST'])
def register():
    if request.method == 'GET':
        return render_template("signup.html")
    else:
        name = request.form['name']
        email = request.form['email']
        #password = request.form['password'].encode('utf-8')
        password = request.form['password']
        rol = 'user'
        #hash_password = bcrypt.hashpw(password, bcrypt.gensalt())

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users (name, email, password,rol) VALUES (%s,%s,%s,%s)",(name,email,password,rol))
        mysql.connection.commit()
        curl = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        curl.execute("SELECT * FROM users WHERE email=%s",(email,))
        user = curl.fetchone()
        session['name'] = user['name']
        session['email'] = user['email']
        session['rol'] = user['rol']
        session['id'] = user['id']

        flash('se registro correctamente')
        return redirect(url_for('index'))
  

@app.route('/registeradmin', methods=['GET', 'POST'])
def registerAdmin():
    if request.method == 'GET':
        return render_template("signup.html")
    else:
        name = request.form['name']
        email = request.form['email']
        #password = request.form['password'].encode('utf-8')
        password = request.form['password']
        rol = 'admin'
        #hash_password = bcrypt.hashpw(password, bcrypt.gensalt())

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users (name, email, password,rol) VALUES (%s,%s,%s,%s)",(name,email,password,rol))
        mysql.connection.commit()
        flash('se registro correctamente')
        return redirect(url_for('listaUsuario'))
        #return render_template("Crud_user.html")
    
@app.route('/formnuevouser',methods=['GET'])
def irNuevoUser():
    return render_template("formularioUserAdmin.html")

@app.route('/formnuevousern',methods=['GET'])
def irNuevoUserN():
    return render_template("formularioUser.html")    

@app.route('/listausuario',methods=['GET'])
def listaUsuario():
    return render_template("Crud_user.html")

@app.route('/logout', methods=["GET", "POST"])
def logout():
    session.clear()
    return render_template("cartillas.html")



#Creando crud de biblioteca

@app.route('/static/biblioteca.html')
def Crud_juegos():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM juegos')
    data = cur.fetchall()
    cur.close()
    return render_template('biblioteca.html', juegos = data)


@app.route('/editG/<id>', methods = ['POST', 'GET'])
def get_juegos(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM juegos WHERE id = %s', [id])
    data = cur.fetchall()
    cur.close()
    print(data[0])
    return render_template('edit-biblioteca.html', juegos = data[0])


@app.route('/deleteG/<string:id>', methods = ['POST','GET'])
def delete_juegos(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM juegos WHERE id = {0}'.format(id))
    mysql.connection.commit()
    flash('juego eliminado con exito')
    return render_template('biblioteca.html')

@app.route('/updateG/<id>', methods=['POST'])
def update_juegos(id):
    if request.method == 'POST':
        name = request.form['name']
        genero = request.form['genero']
        imagen = request.form['imagen']
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE juegos
            SET name = %s,
                genero = %s,
                imagen = %s
            WHERE id = %s
        """, (name, genero, imagen, id))
        flash('Juego actualizado con extito')
        mysql.connection.commit()
        return render_template('Biblioteca.html')        




@app.route('/add_contact', methods=['POST'])
def add_contact():
    if request.method == 'POST':
        serial = request.form['serial']
        gaseosas = request.form['gaseosas']
        risitos = request.form['risitos']
        galletas = request.form['galletas']
        img = request.form['img']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO juegos (serial, gaseosas, risitos, galletas, img) VALUES (%s,%s,%s,%s,%s)", (serial, gaseosas, risitos, galletas, img))
        mysql.connection.commit()
        flash('juego Added successfully')
        return redirect(render_template('biblioteca.html'))



# @app.route('/mostraContrseña/',methods=['GET'])
# def mostrarcontraseña():
#     return render_template("ShowPass.html", users = data[0])





if __name__ == '__main__':
    app.secret_key = "^A%DJAJU^JJ123"
    app.run(debug = True, port= 8000)# Se encarga de ejecutar el servidor 5000



