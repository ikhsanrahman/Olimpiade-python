from server import db
from server import User
import sys

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
	username = input('username> ')
	email = input('email> ')
	password = input('password> ')

	if username and email and password:
		user = User(nama=username, email=email, alamat="", 
                    jenis_kelamin="1", kategori="", 
                    kab_kota="", provinsi="", password=password, role='admin')

		user.confirm_user()
		user.generate_token()
		db.session.add(user)
		db.session.commit()
		print('admin created!')

if sys.argv[1] == 'listadmin':
	admins = User.query.filter_by(role='admin')
	for admin in admins:
		print(admin.nama, admin.email, admin.password)

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
	import random
	import string
	words = [i for i in string.ascii_letters]

	def generate_name():
		return "".join([random.choice(words) for i in range(10)])

	def generate_email():
		return "".join([random.choice(words) for i in range(10)])+"@gmail.com"

	def generate_password():
		return "".join([random.choice(words) for i in range(10)])

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
	app.run()


if sys.argv[1] == 'active':
	users = User.query.filter_by(authenticated=True)
