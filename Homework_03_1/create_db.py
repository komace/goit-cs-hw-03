import psycopg2

def create_db():
    conn = psycopg2.connect(
        host="localhost",
        port="5432",
        dbname="postgres",  
        user="jurek",  
        password="password"  
    )
    conn.autocommit = True
    cursor = conn.cursor()
    
    
    cursor.execute('CREATE DATABASE my1_new_db;')
    cursor.close()
    conn.close()

create_db()


