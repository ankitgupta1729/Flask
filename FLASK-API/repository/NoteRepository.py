import psycopg2

from models.Note import Note

def db_conn():
    return psycopg2.connect(database="flask_database",host="localhost",user="postgres",password="ankit135",port="5432")

def get_all_notes():
    conn=db_conn()
    cur=conn.cursor()
    cur.execute("SELECT * FROM crudTutorial")
    data=cur.fetchall()
    cur.close()
    conn.close()

    notes = [Note(id=row[0],name=row[1],description=row[2]) for row in data]
    return notes

def get_note_by_id(note_id):
    conn=db_conn()
    cur=conn.cursor()
    cur.execute("SELECT * FROM crudTutorial WHERE id=%s",(note_id,))
    data=cur.fetchone()
    cur.close()
    conn.close()

    if data:
        return Note(id=data[0],name=data[1],description=data[2])
    else:
        return None
    
def create_note(name,description):
    conn=db_conn()
    cur=conn.cursor()
    cur.execute("INSERT INTO crudTutorial (name, description) VALUES (%s, %s)", (name,description))
    new_note_id=cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()

    return new_note_id
    
def update_note(note_id,name,description):
    conn=db_conn()
    cur=conn.cursor()
    cur.execute("UPDATE crudTutorial SET name=%s, description=%s WHERE id=%s",(name,description,note_id))
    conn.commit()
    cur.close()
    conn.close()

def delete_note(note_id):
    conn=db_conn()
    cur=conn.cursor()
    cur.execute("DELETE FROM crudTutorial WHERE id=%s",(note_id,))
    conn.commit()
    cur.close()
    conn.close()