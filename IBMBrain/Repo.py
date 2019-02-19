import psycopg2
__name__ = "Repo"
import pandas as pd
#print("Welcome")
defaultquery = ""

def QueryToDataFrame(query):
    connection = CreateDatabaseConnection()
    dfResult = pd.read_sql(query, connection)
    return dfResult

def Main(query):
    connection = CreateDatabaseConnection()
    resultset = ExecuteQuery(connection, query)
    return resultset

def CreateDatabaseConnection():
    #Connection String
    conn = psycopg2.connect(host="localhost",database="Empire", user="Winner", password="winner")
    return conn

def ExecuteQuery(conn, query):
    #Define Cursor
    cursor = conn.cursor()

    #Execute SQL Statement and store result in cursor
    if(query == ""):
        query = defaultquery
    cursor.execute(query)
    rows = cursor.fetchall();
    return rows

def ProcessResultSet():
    for row in rows:
        if not row:
            break
        print(row)

#print("EOP")