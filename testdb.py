from server import db
from server import User, Skor, Soal


"""user = User(nama='anu', email='asaasa', alamat='', 
			sekolah='', jenis_kelamin='', kategori='', 
			kab_kota='', provinsi='', password='')
skor.skor = 121
user.skor_id.append(skor)
db.session.add(user)
db.session.commit()"""

# skor per user


'''
user = User(nama='anu', email='asaddsdsddsdaadsaasa', alamat='', 
			sekolah='', jenis_kelamin='', kategori='', 
			kab_kota='', provinsi='', password='')

skor = Skor()
skor.skor = 10
user.skor_id.append(skor)
db.session.add(user)
db.session.commit()
'''


user = User.query.filter_by(user_id=3).first()

if user.role == 'user':
	# read data
	skor = Skor.query.join(User).filter_by(user_id=user.user_id)
	print(skor)





