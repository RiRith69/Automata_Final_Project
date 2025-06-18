import sys
import os

# Get absolute path to project root and add to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from components.db_connection import db_connection

class FADatabaseHandler:
    def save_fa(self, fa, user_id):
        conn = db_connection()
        if not conn:
            return
        try:
            cursor = conn.cursor()
            insert_script = '''
                INSERT INTO finite_automata(name, type, states, alphabet, start_state, final_states, user_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING fa_id;
            '''
            cursor.execute(insert_script, (
                fa.name, 'DFA' if fa.is_dfa() else 'NFA', fa.states,
                fa.alphabet, fa.start_state, fa.final_states, user_id
            ))
            fa_id = cursor.fetchone()[0]
            conn.commit()
            return fa_id
        except Exception as e:
            print("Save FA error:", e)
            conn.rollback()
        finally:
            cursor.close()
            conn.close()

    def save_transitions(self, fa_id, transitions):
        conn = db_connection()
        if not conn or fa_id == 0:
            return
        try:
            cursor = conn.cursor()
            insert_query = '''
                INSERT INTO transitions(fa_id, from_state, input_symbol, to_states)
                VALUES (%s, %s, %s, %s);
            '''
            for from_state, symbol_dict in transitions.items():
                for symbol, to_states in symbol_dict.items():
                    cursor.execute(insert_query, (fa_id, from_state, symbol, to_states))
            conn.commit()
        except Exception as e:
            print("Save Transitions error:", e)
            conn.rollback()
        finally:
            cursor.close()
            conn.close()

    def load_all_fa_names(self, username):
        conn = db_connection()
        if not conn:
            return
        try:
            cursor = conn.cursor()
            query = '''
                SELECT fa.fa_id, fa.name
                FROM finite_automata fa
                JOIN users u ON fa.user_id = u.user_id
                WHERE u.username = %s;
            '''
            cursor.execute(query, (username,))
            return cursor.fetchall()
        except Exception as e:
            print("Load FA Names error:", e)
        finally:
            cursor.close()
            conn.close()

    def load_fa_by_name(self, fa_name):
        connector = db_connection()
        if connector is None:
            return None

        try:
            cursor = connector.cursor()
            query = '''
                SELECT fa_id, name, type, states, alphabet, start_state, final_states
                FROM finite_automata
                WHERE name = %s
            '''
            cursor.execute(query, (fa_name,))
            result = cursor.fetchone()

            if result:
                fa_id, name, fa_type, states, alphabet, start_state, final_states = result

                # Fetch transitions
                cursor.execute('''
                    SELECT from_state, input_symbol, to_states
                    FROM transitions
                    WHERE fa_id = %s
                ''', (fa_id,))
                raw_transitions = cursor.fetchall()

                # Format transitions into a nested dict: {state: {symbol: [to_states]}}
                transitions = {}
                for from_state, symbol, to_states in raw_transitions:
                    if from_state not in transitions:
                        transitions[from_state] = {}
                    transitions[from_state][symbol] = to_states

                # Return dict compatible with FiniteAutomaton constructor
                return {
                    "name": name,
                    "fa_type": fa_type,
                    "states": states,
                    "alphabet": alphabet,
                    "start_state": start_state,
                    "final_states": final_states,
                    "transitions": transitions
                }

        except Exception as error:
            print(f"Error loading FA: {error}")
            return None
        finally:
            cursor.close()
            connector.close()

    def load_fa_transitions(self, fa_id):
        conn = db_connection()
        if not conn:
            return
        try:
            cursor = conn.cursor()
            query = '''
                SELECT from_state, input_symbol, to_states
                FROM transitions
                WHERE fa_id = %s;
            '''
            cursor.execute(query, (fa_id,))
            return cursor.fetchall()
        except Exception as e:
            print("Load transitions error:", e)
        finally:
            cursor.close()
            conn.close()