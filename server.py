from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    g,
    send_from_directory)

from flask_login import (
    LoginManager,
    login_user,
    logout_user,
    current_user,
    login_required)

from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from werkzeug.utils import secure_filename

import csv
import time

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

app = Flask("admin")

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///prf2.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["UPLOAD_FOLDER"] = "static/img"
app.secret_key = "managaassQW"

db = SQLAlchemy(app)
login = LoginManager(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@login_manager.user_loader
def load_user(user_id):
    return User.query.filter(User.user_id == int(user_id)).first()

class User(db.Model):
    __tablename__ = "users"
    user_id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.Text, index=True)
    email = db.Column(db.Text, unique=True)
    password = db.Column(db.String(200))
    registered_date = db.Column(db.DateTime)
    authenticated = db.Column(db.Boolean, default=False)
    role = db.Column(db.Text, default="user")
    confirmed = db.Column(db.Boolean, default=False)
    token = db.Column(db.Text, unique=True)
    telepon = db.Column(db.Text)
    sekolah = db.Column(db.Text)
    alamat = db.Column(db.Text)
    jenis_kelamin = db.Column(db.Text)
    kategori = db.Column(db.Text)
    kab_kota = db.Column(db.Text)
    provinsi = db.Column(db.Text)
    skor = db.Column(db.Integer)
    skor_id = db.relationship("Skor", backref=db.backref("users", uselist=False), lazy=True)
    answered_soal_id = db.relationship("Soal", backref=db.backref("soal", uselist=False), lazy=True)


    def __init__(self, nama, email, alamat, sekolah,
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
        self.sekolah = sekolah
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

    def undoconfirm_user(self):
        self.confirmed = False

    def get_id(self):
        return str(self.user_id)

    def set_password(self , password):
        self.password = generate_password_hash(password)

    def check_password(self , password):
        return check_password_hash(self.password , password)

    def __repr__(self):
        return "<User %r>"% (self.nama)


class Soal(db.Model):
    __tablename__ = "soal"
    id = db.Column("id_soal", db.Integer, primary_key=True)
    kategori = db.Column(db.Text)
    teks_soal = db.Column(db.Text)
    opsi_a = db.Column(db.Text)
    opsi_b = db.Column(db.Text)
    opsi_c = db.Column(db.Text)
    opsi_d = db.Column(db.Text)
    opsi_benar = db.Column(db.Text)
    gambar = db.Column(db.Text)
    posted_date = db.Column(db.DateTime)
    answered_by = db.Column(db.Integer, db.ForeignKey("users.user_id"))

    def __init__(self, kategori, teks_soal, opsi_a, opsi_b, opsi_c, opsi_d, opsi_benar, gambar):
        self.kategori = kategori
        self.teks_soal = teks_soal
        self.opsi_a = opsi_a
        self.opsi_b = opsi_b
        self.opsi_c = opsi_c
        self.opsi_d = opsi_d
        self.opsi_benar = opsi_benar
        self.gambar = gambar
        self.posted_date = datetime.utcnow()

    def __repr__(self):
        return "<Soal %r>"% (self.id)


class Skor(db.Model):
    __tablename__ = "skor"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    skor = db.Column(db.Integer, default=0)


class Pengumuman(db.Model):
    __tablename__ = "pengumuman"
    id = db.Column("id", db.Integer, primary_key=True)
    kategori = db.Column(db.Text)
    judul = db.Column(db.Text)
    konten = db.Column(db.Text)
    posted_date = db.Column(db.DateTime)

    def __init__(self, kategori, judul, konten):
        self.kategori = kategori
        self.judul = judul
        self.konten = konten
        self.posted_date = datetime.utcnow()


    def __repr__(self):
        return "<Pengumuman %r>"% (self.id)


class Event(db.Model):
    __tablename__ = "event"
    id = db.Column(db.Integer, primary_key=True)
    start = db.Column(db.Float)
    duration = db.Column(db.Integer)
    is_started = db.Column(db.Boolean, default=False)
    stop = db.Column(db.Float)

    def __init__(self, duration):
        self.start = time.time()
        self.duration = duration
        self.stop = self.start + (3600 * self.duration)

    def mulai(self):
        self.is_started = True

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

@app.route('/confirmed')
@login_required
def user_confirmed():
    if current_user.role == "admin":
        user = User.query.filter_by(role='user').filter_by(confirmed=True)
        return render_template("admin.html", confirmed_users=user)

    return redirect(url_for("index_page"))


@app.route("/confirm/<id>", methods=["POST"])
@login_required
def confirm_user(id):
    if current_user.role == "admin":
        if id:
            user = User.query.filter_by(user_id=id).first()
            if user and user.is_confirmed() is not True:
                user.confirm_user()
                user.generate_token()
                print(user.token)
                db.session.commit()
                return redirect(url_for("manage_user"))

    return redirect(url_for("index_page"))


@app.route("/undoconfirm/<id>", methods=["POST"])
@login_required
def undoconfirm_user(id):
    if current_user.role == "admin":
        if id:
            user = User.query.filter_by(user_id=id).first()
            if user and user.is_confirmed():
                user.undoconfirm_user()
                db.session.add(user)
                db.session.commit()
                return redirect(url_for("user_confirmed"))


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
        soal = Soal.query.all()
        return render_template("soal.html", soal=soal)
    # else return forbidden message!


@app.route("/tambahsoal", methods=["GET", "POST"])
@login_required
def tambah_soal():
    if current_user.role == "admin":
        if request.method == "POST":
            kategori = request.form.get("kategori")
            opsi_benar = request.form.get("pilihan_benar")
            teks_soal = request.form["teks_soal"]
            opsi_a = request.form["pilihan_a"]
            opsi_b = request.form["pilihan_b"]
            opsi_c = request.form["pilihan_c"]
            opsi_d = request.form["pilihan_d"]

            if 'file' in request.files:
                file = request.files['file']

                if file.filename == "":
                    return redirect(url_for("add_soal"))

                file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
                soal = Soal(kategori=kategori, teks_soal=teks_soal, opsi_a=opsi_a,
                            opsi_b=opsi_b, opsi_c=opsi_c, opsi_d=opsi_d,
                            opsi_benar=opsi_benar, gambar=file.filename)

                db.session.add(soal)
                db.session.commit()

                return redirect(url_for("add_soal"))

            soal = Soal(kategori=kategori, teks_soal=teks_soal, opsi_a=opsi_a,
                        opsi_b=opsi_b, opsi_c=opsi_c, opsi_d=opsi_d,
                        opsi_benar=opsi_benar, gambar='0')

            db.session.add(soal)
            db.session.commit()

            return redirect(url_for("add_soal"))

        return render_template("tambah_soal.html")

    return redirect(url_for("index_page"))


@app.route("/editsoal/<id>", methods=["GET", "POST"])
def edit_soal(id):
    if current_user.role == "admin":
        if id:
            if request.method == "POST":
                if 'file' in request.files:
                    file = request.files['file']

                    if file and allowed_file(file.filename):
                        kategori = request.form.get("kategori")
                        teks_soal = request.form["teks_soal"]
                        opsi_a = request.form["pilihan_a"]
                        opsi_b = request.form["pilihan_b"]
                        opsi_c = request.form["pilihan_c"]
                        opsi_d = request.form["pilihan_d"]

                        soal = Soal.query.filter_by(id=id).first()

                        soal.kategori = kategori
                        soal.teks_soal = teks_soal
                        soal.opsi_a = opsi_a
                        soal.opsi_b = opsi_b
                        soal.opsi_c = opsi_c
                        soal.opsi_d = opsi_d
                        soal.gambar = file.filename

                        file.save(os.path.join(app.config["UPLOAD_FOLDER"], file.filename))

                        db.session.commit()
                        return redirect(url_for("add_soal"))

                kategori = request.form.get("kategori")
                teks_soal = request.form["teks_soal"]
                opsi_a = request.form["pilihan_a"]
                opsi_b = request.form["pilihan_b"]
                opsi_c = request.form["pilihan_c"]
                opsi_d = request.form["pilihan_d"]

                soal = Soal.query.filter_by(id=id).first()

                soal.kategori = kategori
                soal.teks_soal = teks_soal
                soal.opsi_a = opsi_a
                soal.opsi_b = opsi_b
                soal.opsi_c = opsi_c
                soal.opsi_d = opsi_d

                db.session.commit()
                return redirect(url_for("add_soal"))


            soal = Soal.query.filter_by(id=id).first()

            if soal:
                return render_template("editsoal.html", soal=soal)

            return redirect(url_for("add_soal"))

        return redirect(url_for("add_soal"))


@app.route("/deletesoal/<id>", methods=["POST"])
def delete_soal(id):
    if current_user.role == "admin":
        if id:
            if request.method == "POST":
                soal = Soal.query.filter_by(id=id).first()
                if soal:
                    db.session.delete(soal)
                    db.session.commit()
                    return redirect(url_for("add_soal"))
                return redirect(url_for("add_soal"))


@app.route("/pengumuman")
@login_required
def pengumuman():
    if current_user.role == "admin":
        pengumuman = Pengumuman.query.all()
        return render_template("pengumuman.html", pengumuman=pengumuman)

    return redirect(url_for("index_page"))



@app.route("/tambahpengumuman", methods=["GET", "POST"])
@login_required
def tambah_pengumuman():
    if current_user.role == "admin":
        if request.method == "POST":
            kategori = request.form.get("kategori")
            judul = request.form["judul"]
            konten = request.form["konten"]

            pengumuman = Pengumuman(kategori=kategori, judul=judul, konten=konten)
            db.session.add(pengumuman)
            db.session.commit()

            return redirect(url_for("pengumuman"))

        return render_template("tambah_pengumuman.html")


@app.route("/editpengumuman/<id>", methods=["GET", "POST"])
def edit_pengumuman(id):
    if current_user.role == "admin":
        if id:
            if request.method == "POST":
                kategori = request.form.get("kategori")
                judul = request.form["judul"]
                konten = request.form["konten"]

                pengumuman = Pengumuman.query.filter_by(id=id).first()

                pengumuman.kategori = kategori
                pengumuman.judul = judul
                pengumuman.konten = konten

                db.session.commit()

                return redirect(url_for("pengumuman"))

            pengumuman = Pengumuman.query.filter_by(id=id).first()

            if pengumuman:
                return render_template("editpengumuman.html", pengumuman=pengumuman)

            return redirect(url_for("pengumuman"))

        return redirect(url_for("pengumuman"))


@app.route("/deletepengumuman/<id>", methods=["POST"])
def delete_pengumuman(id):
    if current_user.role == "admin":
        if id:
            if request.method == "POST":
                pengumuman = Pengumuman.query.filter_by(id=id).first()
                if pengumuman:
                    db.session.delete(pengumuman)
                    db.session.commit()
                    return redirect(url_for("pengumuman"))

                return redirect(url_for("pengumuman"))





@app.route("/download/peserta")
@login_required
def download_peserta():

    if current_user.role == "admin":
        data_user = User.query.filter_by(confirmed=True)

        with open("static/datapeserta.csv", "w+") as f:
            writer = csv.writer(f, delimiter=";")
            writer.writerow(("nama", "email", "registered_date", "alamat", "sekolah", "jenis_kelamin", "kategori", "kab_kota", "provinsi"))

            for user in data_user:
                writer.writerow((user.nama, user.email, user.registered_date, user.alamat,
                                 user.sekolah, user.jenis_kelamin, user.kategori, user.kab_kota, user.provinsi))

        return send_from_directory(directory="static", filename="datapeserta.csv")


@app.route("/download/pendaftar")
@login_required
def download_pendaftar():
    if current_user.role == "admin":
        data_user = User.query.filter_by(confirmed=False)

        with open("static/datapendaftar.csv", "w+") as f:
            writer = csv.writer(f, delimiter=";")
            writer.writerow(("nama", "email", "registered_date", "alamat", "sekolah", "jenis_kelamin", "kategori", "kab_kota", "provinsi"))

            for user in data_user:
                writer.writerow((user.nama, user.email, user.registered_date, user.alamat, user.sekolah, user.jenis_kelamin, user.kategori, user.kab_kota, user.provinsi))

        return send_from_directory(directory="static", filename="datapendaftar.csv")


@app.route("/download")
@login_required
def download():
    if current_user.role == "admin":
        return render_template("download.html")



@app.route("/event", methods=["GET", "POST"])
@login_required
def event_manager():
    if current_user.role == "admin":
        if request.method == "POST":
            duration = request.form.get('durasi')
            event = Event(duration=int(duration))
            db.session.add(event)
            db.session.commit()
            return redirect(url_for("event_manager"))

        events = Event.query.all()
        return render_template("event.html", events=events)



@app.route("/startevent/<id>", methods=["POST"])
@login_required
def start_event():
    if current_user.role == "admin":
        if request.method == "POST":
            event = Event.query.filter_by(id=id).first()
            if event:
                event.is_started = True
                db.session.commit()
                return redirect(url_for("event_manager"))



@app.route("/hapusevent/<id>", methods=["POST"])
@login_required
def hapus_event(id):
    if current_user.role == "admin":
        if request.method == "POST":
            even = Event.query.filter_by(id=id).first()
            if event:
                db.session.delete(event)
                db.session.commit()
                return redirect(url_for("event_manager"))

    return redirect(url_for("main_app"))


################################
# USER AREA
################################


@app.route("/index", methods=["GET"])
@app.route("/index.html", methods=["GET"])
@app.route("/", methods=["GET"])
def index_page():
   return render_template("index.html", title="Selamat datang di PRF Nasional")


@app.route("/login", methods=["GET", "POST"])
@app.route("/login.html", methods=["GET"])
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

        return render_template("login.html", message="Email atau password anda salah!", title="Login")


        #return redirect(url_for("login"))
    return render_template("login.html", title="Login")


@app.route("/app", methods=["GET"])
@login_required
def main_app():
    if current_user.role == "user":
        pengumuman = Pengumuman.query.all()
        return render_template("app.html", title="selamat datang di PRF Nasional!", pengumuman=pengumuman)
    # return 403 error


@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":
        nama = request.form["nama"]
        email = request.form["email"]
        password = request.form["password"]
        alamat = request.form["alamat"]
        nama_sekolah = request.form["nama_sekolah"]
        jenis_kelamin = request.form.get("jenis_kelamin")
        kategori = request.form.get("kategori")
        kab_kota = request.form["kabupaten_kota"]
        provinsi = request.form.get("provinsi")

        if not User.query.filter_by(email=email).first():

            user = User(nama=nama, email=email, alamat=alamat, sekolah=nama_sekolah,
                        jenis_kelamin=jenis_kelamin, kategori=kategori,
                        kab_kota=kab_kota, provinsi=provinsi, password=password)

            db.session.add(user)
            db.session.commit()
            return render_template("register_success.html", nama=nama, title="Registrasi Berhasil!")

        else:
            return render_template("register.html", msg="email sudah terdaftar")

    return render_template("register.html", title="Registrasi")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index_page"))


@app.route("/periksa/<id>", methods=["POST"])
@login_required
def periksa_soal(id):

    if current_user.role == "user":
        if request.method == "POST":

            soal = Soal.query.filter_by(id=id).first()

            if request.form.get("pilihan") == soal.opsi_benar:

                skor = Skor.query.join(User).filter_by(user_id=current_user.user_id).first()
                jawaban = request.form.get("pilihan")
                soal = Soal.query.filter_by(soal_id=id).first()

                if jawaban == soal.opsi_benar:
                    skor.skor += 4
                else:
                    skor.skor -= 1

                db.session.commit()

                return jsonify({"status": "200 OK"})


@app.route("/lomba", methods=["GET", "POST"])
@login_required
def mulai_lomba():
    if current_user.role == "user":
        soal = Soal.query.filter_by(kategori=current_user.kategori)
        return render_template("lomba.html", soal=soal)

    return redirect(url_for("login"))


@app.route("/info")
@login_required
def user_info():
    if current_user.role == "user":
        return render_template("infopeserta.html", title="Informasi Personal Peserta")

    # return 403 error


@app.route("/scoreboard")
def scoreboard():
    skor = Skor.query.order_by(Skor.skor.desc())
    return render_template("skorboard.html", skor=skor)
