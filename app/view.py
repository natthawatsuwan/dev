import psycopg2
from psycopg2 import Error

try:
    connection = psycopg2.connect(user = "postgres",
                                  password = "postgres",
                                  host = "127.0.0.1",
                                  port = "5432",
                                  database = "postgres")

    cursor = connection.cursor()
    
    create_table_query = '''SELECT * From person'''
    
    cursor.execute(create_table_query)
    connection.commit()
    print("show person successfully in PostgreSQL ")

except Exception as e:
    print(e)
except (Exception, psycopg2.Error) as error :
                                             print ("Error while connecting to PostgreSQL", error)
finally:
    #closing database connection.
        if(connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")