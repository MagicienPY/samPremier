import pymysql

con = pymysql.connect(user='root', password ='',database = 'gestage')
cursor = con.cursor()

query = 'select * from stagiaire;'

r = cursor.execute(query)