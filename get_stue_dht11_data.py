import sqlite3
def get_TOF_data(number_of_rows):
    query = """SELECT * FROM TOF ORDER BY Dato DESC;"""  
    Dato = []
    Temp = []
    Hum = []
    conn = None  

    try:
        conn = sqlite3.connect("database/Temp.db")
        cur = conn.cursor()
        cur.execute(query)
        rows = cur.fetchmany(number_of_rows)
        
        for row in rows:
            Temp.append(row[0])
            Hum.append(row[1])
            Dato.append(row[2])
            
        return Dato, Temp, Hum

    except sqlite3.Error as sql_e:
        print(f"sqlite error occurred: {sql_e}")
        return [], [], []

    except Exception as e:
        print(f"Error occurred: {e}")
        return [], [], []

    finally:
        if conn:  
            conn.close()
