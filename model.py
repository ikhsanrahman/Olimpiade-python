from flask_sqlalchemy import SQLAlchemy 
from server import app

class User(db.Model):
    __tablename__ = "users"
    id = db.Column("user_id", db.Integer, primary_key=True)
    nama = db.Column("username", db.Text, index=True)
    email = db.Column("email", db.Text, unique=True)
    password = db.Column("password", db.String(200))
    registered_date = db.Column("registered_date", db.DateTime)
    authenticated = db.Column(db.Boolean, default=False)
    role = db.Column(db.Text, default="user")
    confirmed = db.Column(db.Boolean, default=False)
    token = db.Column(db.Text, unique=True)
    telepon = db.Column('telepon', db.Text)
    sekolah = db.Column('sekolah', db.Text)
    alamat = db.Column('alamat', db.Text)
    jenis_kelamin = db.Column('jenis_kelamin', db.Text)
    kategori = db.Column('kategori', db.Text)
    kab_kota = db.Column('kab_kota', db.Text)
    provinsi = db.Column('provinsi', db.Text)
    #skor_id = db.relationship("Skor", backref="user", lazy=True)


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
    kategori = db.Column(db.Text)
    teks_soal = db.Column(db.Text)
    opsi_a = db.Column(db.Text)
    opsi_b = db.Column(db.Text)
    opsi_c = db.Column(db.Text)
    opsi_d = db.Column(db.Text)
    opsi_benar = db.Column(db.Text)
    posted_date = db.Column(db.DateTime)

    def __init__(self, kategori, teks_soal, opsi_a, opsi_b, opsi_c, opsi_d, opsi_benar):
        self.kategori = kategori
        self.teks_soal = teks_soal
        self.opsi_a = opsi_a
        self.opsi_b = opsi_b
        self.opsi_c = opsi_c
        self.opsi_d = opsi_d
        self.opsi_benar = opsi_benar
        self.posted_date = datetime.utcnow()

    def __repr__(self):
        return "<Soal %r>"% (self.id)


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


class Lomba(db.Model):
    __tablename__ = "lomba"
    id = db.Column(db.Integer, primary_key=True)
    mulai = db.Column(db.Boolean, default=False)
    start = db.Column(db.DateTime)
    durasi = db.Column(db.Integer)

    def __init__(self, start, durasi):
        self.mulai = False
        self.start = start
        self.durasi = durasi


    def mulai_lomba(self):
        self.start = True


class Skor(db.Model):
    __tablename__ = "skor"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    skor = db.Column(db.Integer, default=0)

    def __init__(self):
        pass

    def tambah_skor_benar(self):
        self.skor += 4

    def kurang_skor_salah(self):
        self.skor -= 1


class SkoringRule(db.Model):
    __tablename__ = "skoring_rule"
    id = db.Column(db.Integer, primary_key=True)
    skor_benar = db.Column(db.Integer)
    skor_salah = db.Column(db.Integer)
    skor_kosong = db.Column(db.Integer)


class Event(db.Model):
    __tablename__ = "event"
    id = db.Column(db.Integer, primary_key=True)
    start = db.Column(db.DateTime)
    duration = db.Column(db.Integer)
    is_started = db.Column(db.Boolean, default=False)

    def __init__(self, duration):
        self.start = datetime.utcnow()
        self.duration = duration

    def mulai(self):
        self.is_started = True