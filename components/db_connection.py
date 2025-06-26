import psycopg2

# database info
host = 'localhost'
database = 'finite_automata'
username = 'team_leader'
pw = 'TL0123'
port_id = 5432

# Connect to database
def get_db_connection() :
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
