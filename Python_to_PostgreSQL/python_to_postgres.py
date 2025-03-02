import psycopg2
import psycopg2.extras # if table has has many columns like 100s of columns then we need to 
#return data in the form of dictionary

host = "localhost"
database = "flask_database"
username="postgres"
password="ankit135"
port_id="5432"
conn=None
cur=None
# in real time, we don't use these variables. We create configuration file and use it in our file

try:
    conn=psycopg2.connect(host=host,database=database,user=username,password=password,port=port_id)
    print("Connection established successfully")
    cur=conn.cursor(cursor_factory=psycopg2.extras.DictCursor) # a cursor is used to perform SQL operations

    cur.execute("DROP TABLE IF EXISTS employee")
    conn.commit()
    
    create_script='''CREATE TABLE IF NOT EXISTS employee(
                        id int PRIMARY KEY,
                        name varchar(40) NOT NULL,
                        salary int,
                        dept_id varchar(30))'''
    cur.execute(create_script)
    conn.commit()
    print("Table created successfully")

    insert_script='''INSERT INTO employee(id,name,salary,dept_id) VALUES(%s,%s,%s,%s)'''
    insert_value=[(1,'Ankit',10000,'IT'),
                  (2,'Rahul',20000,'HR'),
                  (3,'Rohit',30000,'IT'),
                  (4,'Raj',40000,'HR'),
                  (5,'Ravi',50000,'IT')]
    for  record in insert_value:
        cur.execute(insert_script,record)
    conn.commit()
    print("Data inserted successfully")

    cur.execute("SELECT * FROM employee")
    rows=cur.fetchall() # use fetchone() to get only one row
    print("Data from table: ")
    for row in rows:
        print(row)
    for row in rows:
        print(row[1],row[2])
    for row in rows:
        print(row['name'],row['salary'])
    print("Data fetched successfully")

    update_script='UPDATE employee SET salary=salary+(salary*0.5)'
    cur.execute(update_script)
    cur.execute("SELECT * FROM employee")
    for record in cur.fetchall():
        print(record['name'],record['salary'])
    print("Data updated successfully")
    conn.commit()

    delete_script='DELETE FROM employee WHERE name=%s'
    delete_record=('Raj',)
    cur.execute(delete_script,delete_record)
    cur.execute("SELECT * FROM employee")   
    for record in cur.fetchall():
        print(record)
    print("Data deleted successfully")
    conn.commit()

except Exception as error:
    print("Error: ",error)
    
finally:
    if cur is not None:
        cur.close() # we can use "with" clause then we don't have to use close() or commit()
    if conn is not None:
        conn.close()