import mysql.connector

connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",   # empty password
    database="food_sharing"
)

print("✅ Connected successfully")



