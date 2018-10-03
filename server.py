from flask import (
    Flask, 
    render_template, 
    request, 
    redirect, 
    url_for, 
    flash, 
    g)

from flask_login import (
    LoginManager, 
    login_user, 
    logout_user, 
    current_user, 
    login_required)

from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

app = Flask("admin")

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///testxjx.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = "managaassQW"

db = SQLAlchemy(app)
login = LoginManager(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.filter(User.id == int(user_id)).first()

class User(db.Model):
    __tablename__ = "users"
    id = db.Column("user_id", db.Integer, primary_key=True)
    nama = db.Column("username", db.Text, index=True)
    email = db.Column("email", db.Text, unique=True)
    password = db.Column("password", db.Text, unique=True)
    registered_date = db.Column("registered_date", db.DateTime)
    authenticated = db.Column(db.Boolean, default=False)
    role = db.Column(db.String, default="user")
    confirmed = db.Column(db.Boolean, default=False)
    token = db.Column(db.String, unique=True)
    telepon = db.Column('telepon', db.Text)
    alamat = db.Column('alamat', db.Text)
    jenis_kelamin = db.Column('jenis_kelamin', db.Text)
    kategori = db.Column('kategori', db.Text)
    kab_kota = db.Column('kab_kota', db.Text)
    provinsi = db.Column('provinsi', db.Text)


    def __init__(self, nama, email, alamat, 
                 jenis_kelamin, kategori, kab_kota, provinsi,
                 password, role="user", confirmed=False, authenticated=False):

        self.nama = nama
        self.set_password(password)
        self.email = email
        self.role = role
        self.registered_date = datetime.utcnow()
        self.authenticated = False
        self.confirmed = False
        self.token = None
        self.alamat = alamat
        self.jenis_kelamin = jenis_kelamin
        self.kategori = kategori
        self.kab_kota = kab_kota
        self.provinsi = provinsi

    
    def generate_token(self):

        from random import shuffle, choice
        from hashlib import md5

        import string

        words = [letter for letter in string.ascii_letters]
        shuffle(words)
        random_words = "".join([choice(words) for i in range(10)])

        def generate_md5(letters):
            return md5(str.encode(letters)).hexdigest()

        md5sum = generate_md5(random_words)
        token = "prf-" + md5sum
        self.token = token


    def is_active(self):
        return True


    def is_authenticated(self):
        return True 


    def is_anonymous(self):
        return True 


    def check_password(self, password):
        return check_password(self.password, password)


    def is_confirmed(self):
        return self.confirmed


    def confirm_user(self):
        self.confirmed = True

    def get_id(self):
        return str(self.id)

    def set_password(self , password):
        self.password = generate_password_hash(password)

    def check_password(self , password):
        return check_password_hash(self.password , password)

    def __repr__(self):
        return "<User %r>"% (self.nama)


class Soal(db.Model):
    __tablename__ = "soal"
    id = db.Column("id_soal", db.Integer, primary_key=True)
    kategori = db.Column("kategori", db.Integer)
    teks_soal = db.Column("teks_soal", db.Text)

    def __init__(self, kategori, teks_soal):
        self.kategori = kategori
        self.teks_soal = teks_soal


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        
        email = request.form["email"]
        password = request.form["password"]

        user = User.query.filter_by(email=email).first()

        if user is not None and user.check_password(password) is True:

            user.is_authenticated = True

            db.session.add(user)
            db.session.commit()

            login_user(user)
            
            if user.role == "admin":
                return redirect(url_for('administrator'))

            return redirect(url_for("main_app"))


        return redirect(url_for("login"))
    return render_template("login.html", title="Login")


@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":
        nama = request.form["nama"]
        email = request.form["email"]
        password = request.form["password"]
        alamat = request.form["alamat"]
        jenis_kelamin = request.form.get("jenis_kelamin")
        kategori = request.form.get("kategori")
        kab_kota = request.form["kabupaten_kota"]
        provinsi = request.form.get("provinsi")

        if not User.query.filter_by(email=email).first():
            
            user = User(nama=nama, email=email, alamat=alamat, 
                        jenis_kelamin=jenis_kelamin, kategori=kategori, 
                        kab_kota=kab_kota, provinsi=provinsi, password=password)

            db.session.add(user)
            db.session.commit()
            return render_template("register_success.html", nama=nama, title="Registrasi Berhasil!")


    return render_template("register.html", title="Registrasi Berhasil!")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index_page"))

############################################################
# ADMIN AREA
############################################################

@app.route("/admin")
@login_required
def administrator():

    if current_user.role == "admin":

        peserta = User.query.filter_by(role='user').filter_by(confirmed=True).count()
        pendaftar = User.query.filter_by(role='user').filter_by(confirmed=False).count()

        return render_template("admin.html", peserta=peserta, pendaftar=pendaftar)

    return redirect(url_for("main_app"))


@app.route("/manageuser")
@login_required
def manage_user():
    if current_user.role == "admin":
        users = User.query.filter_by(role='user').filter_by(confirmed=False)
        return render_template("admin.html", users=users)



@app.route("/soal")
@login_required
def add_soal():
    if current_user.role == "admin":
        return render_template("soal.html")
    # else return forbidden message!


@app.route("/confirm/<id>", methods=["POST"])
@login_required
def confirm_user(id):
    if current_user.role == "admin":
        if id:
            user = User.query.filter_by(id=id).first()
            if user is not None and user.is_confirmed() is not True:
                user.confirm_user()
                user.generate_token()
                print(user.token)
                db.session.add(user)
                db.session.commit()
                return redirect(url_for("manage_user"))

@app.route('/confirmed')
@login_required
def user_confirmed():
    if current_user.role == "admin":
        user = User.query.filter_by(role='user').filter_by(confirmed=True)
        return render_template("admin.html", confirmed_users=user)



################################
# USER AREA
################################

@app.route("/", methods=["GET"])
def index_page():
   return render_template("index.html", title="Selamat datang di PRF Nasional")



@app.route("/info")
@login_required
def user_info():
    if current_user.role == "user":
        return render_template("infopeserta.html", title="Informasi Personal Peserta")

    # return 403 error


@app.route("/app", methods=["GET"])
@login_required
def main_app():
    if current_user.role == "user":
        return render_template("app.html", title="selamat datang di PRF Nasional!")
    # return 403 error