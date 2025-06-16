import psycopg2

# database info
host = 'localhost'
database = 'automata_db'
username = 'postgres'
pw = '$@7#Y@'
port_id = 5432

# Connect to database
def db_connection() :
    try :
        connection = psycopg2.connect(
            host = host,
            database = database,
            user = username,
            password = pw,
            port = port_id
        )
        return connection
    except Exception as error :
        print(f"Error at : {error}")
        return None
