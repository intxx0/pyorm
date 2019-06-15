from os import *
from Db import *
from DbMapper import *

class Usuarios(DbMapper):
	name = 'usuarios'

if __name__ == "__main__":
	
	database = Db({'hostname': '192.168.6.96', 'username': 'dev', 'password': 'dev', 'database': 'ecentry_erp'})
	
	# SELECT statements
	
	usuarios = Usuarios(database)
	
	usuarios.fields(('t1.id', 't1.nome', 't2.nome AS empresa'))
	usuarios.join_inner('empresas t2', 't1.id_empresa = t2.id')
	usuarios.order('t1.id')
	usuarios.group('t1.id')
	
	rowset = usuarios.fetch_all()
	
	for row in rowset:
		print row.id
		print row.nome
		print row.empresa
		
	usuarios.where('t1.id', '=', '1')
	
	row = usuarios.fetch_row()
	
	print 'id=' + str(row.id) + ' nome=' + row.nome + "\n"
	
	# UPDATE statements
	
	usuarios = Usuarios(database)
	
	usuarios.fields(('t1.id', 't1.nome'))
	usuarios.where('t1.id', '=', '13')
	
	row = usuarios.fetch_row()
	
	row.nome = 'Test2'
	
	usuarios.save(row)
	
	database.commit()
	
	usuario = Model()
	
	usuario.nome = 'User Test'
	usuario.email = 'teste@teste.com.br'
	usuario.senha = 'test'
	usuario.status = 1
	
	usuarios.save(usuario)
	
	database.commit()
	
	usuarios.delete('id', '=', 18)
	
	database.commit()
	
	
	
