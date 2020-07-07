import mysql.connector

db = mysql.connector.connect (
    host="johnny.heliohost.org",
    user="silashw",
    passwd="elephantCode88",
    database="silashw_levelsData"
)

cursor = db.cursor()

cursor.execute("SELECT * FROM members")

for x in cursor:
    print(x)