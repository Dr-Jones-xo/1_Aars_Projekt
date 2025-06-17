import sqlite3
from Dato import Dato
from random import randint
from time import sleep

sqlite3.register_adapter(Dato, lambda dt: dt.isoformat())

def create_table():
    query = """CREATE TABLE IF NOT EXISTS TOF (
        Temp REAL NOT NULL, 
        Hum REAL NOT NULL, 
        Dato TEXT NOT NULL
    )"""
    
    try:
        conn = sqlite3.connect("database/Temp.db")
        cur = conn.cursor()
        cur.execute(query)
        conn.commit()
    except sqlite3.Error as sql_e:
        print(f"sqlite error occurred: {sql_e}")
    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        conn.close()

def log_stue_DHT11():
    while True:
        query = """INSERT INTO TOF (Temp, Hum, Dato) VALUES (?, ?, ?)"""
        temp = randint(0, 30)
        hum = randint(0, 100)
        now = Dato.now().strftime("%d/%m/%y %H:%M:%S")
        data = (temp, hum, now)  

        try:
            conn = sqlite3.connect("database/Temp.db")
            cur = conn.cursor()
            cur.execute(query, data)
            conn.commit()
        except sqlite3.Error as sql_e:
            print(f"sqlite error occurred: {sql_e}")
            conn.rollback()
        except Exception as e:
            print(f"Error occurred: {e}")
        finally:
            conn.close()
        
        sleep(1)

create_table()

log_stue_DHT11()
