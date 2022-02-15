import pymysql

HOST = ""
PORT = 3306
USER = ""
PASSWORD = ""
DB = ""

conn = pymysql.connect(host=HOST, user=USER, port=PORT, passwd=PASSWORD, db=DB)
