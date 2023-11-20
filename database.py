import mysql.connector

# database details

db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="sqllogin",
    database="passman"
)

crsr = db.cursor()

crsr.execute(
    "CREATE TABLE IF NOT EXISTS users(userid varchar(5) primary key, username varchar(20), password varchar(15))")

crsr.execute("CREATE TABLE IF NOT EXISTS newfeat(SrNo int primary key auto_increment, feat varchar(1000))")

crsr.execute("CREATE TABLE IF NOT EXISTS feedback(SrNo int primary key auto_increment, msg varchar(1000))")
