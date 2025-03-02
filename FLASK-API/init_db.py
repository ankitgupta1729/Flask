import psycopg2

conn = psycopg2.connect(database="flask_database",host="localhost",user="postgres",password="ankit135",port="5432")
cur=conn.cursor()

cur.execute("CREATE TABLE IF NOT EXISTS crudTutorial(id serial PRIMARY KEY, name VARCHAR(100), description VARCHAR(500))")

cur.execute("INSERT INTO crudTutorial (name, description) VALUES (%s, %s)", ("Ankit", "I am a software engineer"))

conn.commit()

cur.close()
conn.close()