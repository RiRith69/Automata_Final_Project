import bcrypt
import streamlit as st
from .db_connection import get_db_connection
from .User_model import User

class UserHandling:
    def __init__(self):
        pass

    def add_user(self, username, password, recovery = None):
        connector = get_db_connection()
        if connector is None:
            return

        try:
            cursor = connector.cursor()

            user = User(username, password, recovery)
            hashed_pw = bcrypt.hashpw(user.password.encode(), bcrypt.gensalt()).decode()

            insert_script = '''
                INSERT INTO users (username, password, recovery)
                VALUES (%s, %s, %s)
                RETURNING user_id;
            '''
            insert_values = (user.username, hashed_pw, user.recovery)
            cursor.execute(insert_script, insert_values)

            user_id = cursor.fetchone()[0]
            connector.commit()

            return user_id

        except Exception as error:
            st.warning(f"⚠️ Error saving user: {error}")

        finally:
            cursor.close()
            connector.close()

    def load_users(self):
        connector = get_db_connection()
        if connector is None:
            return []

        try:
            cursor = connector.cursor()
            query = 'SELECT username FROM users;'
            cursor.execute(query)
            return [row[0] for row in cursor.fetchall()]

        except Exception as error:
            st.warning(f"⚠️ Error loading users: {error}")
            return []

        finally:
            cursor.close()
            connector.close()

    def get_user(self, username):
        connector = get_db_connection()
        if connector is None:
            return None

        try:
            cursor = connector.cursor()
            query = 'SELECT * FROM users WHERE username = %s;'
            cursor.execute(query, (username,))
            return cursor.fetchall()  # will return [(user_id, username, password, recovery, ...)]

        except Exception as error:
            st.warning(f"⚠️ Error loading user: {error}")
            return None

        finally:
            cursor.close()
            connector.close()
