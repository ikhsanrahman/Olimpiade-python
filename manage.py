#!/home/dasta/anaconda3/bin/python


from server import db
from server import User
import sys
import os

import random
import string
words = [i for i in string.ascii_letters]

def generate_name():
	return "".join([random.choice(words) for i in range(10)])

def generate_email():
	return "".join([random.choice(words) for i in range(10)])+"@gmail.com"

def generate_password():
	return "".join([random.choice(words) for i in range(10)])

def generate_password():
	return "".join([random.choice(words) for i in range(10)])


if sys.argv[1] == 'migrate':
	db.create_all()
	print('migrate success!')

if sys.argv[1] == 'drop':
	confirm = input('are you sure? ')\

	if confirm:
		db.drop_all()
		print('tables droped!')


if sys.argv[1] == 'log':
	users = User.query.all()
	
	for user in users:
		print(user.id, user.nama, user.email, user.role, user.registered_date, user.token, user.confirmed)

if sys.argv[1] == 'userconfirmed':
	users = User.query.filter_by(confirmed=True)
	for user in users:
		print(user.id, user.nama, user.email, user.registered_date, user.token)

if sys.argv[1] == 'addadmin':
	username = "adminn"
	email = "admin"
	password = "admin"

	if username and email and password:
		user = User(nama=username, email=email, alamat="WEW", 
                    sekolah="", jenis_kelamin="1", kategori="", 
                    kab_kota="", provinsi=	"", password=password, role='admin')

		user.confirm_user()
		user.generate_token()
		db.session.add(user)
		db.session.commit()
		print('admin created!')

if sys.argv[1] == 'listadmin':
	admins = User.query.filter_by(role='admin')
	for admin in admins:
		print(admin.nama, admin.email, admin.password, admin.role)

if sys.argv[1] == 'testuser':
	username = input('username> ')
	email = input('email> ')
	password = input('password> ')
	if username and email and password:
		user = User(nama=username, email=email, password=password)
		user.generate_token()
		db.session.add(user)
		db.session.commit()
		print('user created!')

if sys.argv[1] == 'confirm':
	id = input('id> ')
	user = User.query.filter_by(id=int(id)).first()
	if user is not None and user.is_confirmed() is not True:
		user.confirm_user()
		user.generate_token()
		db.session.add(user)
		db.session.commit()
		print(user.is_confirmed())
		print('user with id={id} is confirmed'.format(id))

if sys.argv[1] == 'dummy':
	

	for i in range(1000):
		nama=generate_name()
		email=generate_email()
		password=generate_password()

		user = User(nama=nama, email=email, password=password)
		db.session.add(user)
		db.session.commit()
		print('user => {nama} {email} {password} generated!'.format(nama,email,password))

	print('done!')

if sys.argv[1] == 'stats':
	print(User.query.filter_by(confirmed=True).filter_by(role='user').count())
	print(User.query.filter_by(confirmed=True).count())
	print(User.query.filter_by(confirmed=False).count())


if sys.argv[1] == 'run':
	from server import app
	app.run(port=9000, debug=True)


if sys.argv[1] == 'active':
	users = User.query.filter_by(authenticated=True)


if sys.argv[1] == 'adduser':
	username = "adi"
	email = "adi@gmail.com"
	password = "adi"

	if username and email and password:
		user = User(nama=username, email=email, alamat="", sekolah="", 
                    jenis_kelamin="1", kategori="", 
                    kab_kota="", provinsi="", password=password, role='admin')

		user.confirm_user()
		user.generate_token()
		db.session.add(user)
		db.session.commit()
		print('admin created!')


if sys.argv[1] == 'deploy':
	print("deploy system...	")
	os.system("gunicorn server:app -b 'localhost:8000' -w {} ".format(os.cpu_count()))


if sys.argv[1] == 'mulailomba':
	print('memulai lomba')
	from server import Event
	event = Event.query.filter_by(id=1).first()
	print(event.is_started)
	event.mulai()
	print(event.is_started)
	db.session.commit()
