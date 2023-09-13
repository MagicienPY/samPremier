from pyfirmata import Arduino, util
#import MySQLdb
import time
import pymysql

import datetime
date1 = datetime.date.today()




carte = Arduino('/dev/ttyACM0')

acquisition = util.Iterator(carte)

acquisition.start()

tenssio =  carte.get_pin('a:0:i')


time.sleep(1.0)


tenssion  =  tenssio.read()

print(tenssion)




con = pymysql.connect(user='root', password ='',database = 'locus_aia')
cursor = con.cursor()

query = 'insert into resistance values (%s,%s);'

r = cursor.execute(query,(tenssion,date1))
con.commit()
cursor.close()



carte.exit()