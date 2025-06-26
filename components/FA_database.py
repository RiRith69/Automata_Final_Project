import sys
import os
import json
from collections import defaultdict
import streamlit as st

# Get absolute path to project root and add to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from components.db_connection import get_db_connection

class FADatabaseHandler:
    def save_fa(self, fa, user_id):
        conn = None
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute("""
            INSERT INTO finite_automata (name, states, alphabet, start_state, final_states, fa_type, user_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING fa_id
            """, (fa.name, fa.states, fa.alphabet, fa.start_state, fa.final_states, fa.fa_type, user_id[0]))
            
            fa_id = cur.fetchone()[0]
            for from_state, trans in fa.transitions.items():
                for symbol, to_states_list in trans.items():
                    if not isinstance(to_states_list, list):
                        to_states_list = [to_states_list]

                    cur.execute("""
                    INSERT INTO transitions (fa_id, from_state, symbol, to_states)
                    VALUES (%s, %s, %s, %s)
                    """, (fa_id, from_state, symbol, to_states_list))
            
            conn.commit()
            return fa_id
        except Exception as e:
            st.error(f"Database error: {str(e)}")
            return None
        finally:
            if cur :
                cur.close()
            if conn:
                conn.close()


    def load_all_fa_names(self, username):
        conn = get_db_connection()
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
            if cursor :
                cursor.close()
            if conn :
                conn.close()

    def load_fa_info(self, fa_name):
        connector = get_db_connection()
        if connector is None:
            return None

        try:
            cursor = connector.cursor()
            query = '''
                SELECT fa_id, name, fa_type, states, alphabet, start_state, final_states
                FROM finite_automata
                WHERE name = %s
            '''
            cursor.execute(query, (fa_name,))
            fa_data = cursor.fetchone()
            if not fa_data :
                return
            # Load transitions
            cursor.execute("""
                SELECT from_state, symbol, to_states
                FROM transitions
                WHERE fa_id = %s
                ORDER BY from_state, symbol
            """, (fa_data[0],))
            
            transitions = defaultdict(lambda: defaultdict(list))
            for from_state, symbol, to_state in cursor.fetchall():
                transitions[from_state][symbol].append(to_state)
        
            return {
                'id': fa_data[0],
                'name': fa_data[1],
                'type': fa_data[2],
                'states': fa_data[3],
                'alphabet': fa_data[4],
                'start_state': fa_data[5],
                'final_states': fa_data[6],
                'transitions': dict(transitions)
            }

        except Exception as error:
            print(f"Error loading FA: {error}")
            return None
        finally:
            if cursor :
                cursor.close()
            if connector :
                connector.close()
    def show_transition_table(self, fa_id):
        conn = None
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            
            # Get the FA first to access states and alphabet
            cur.execute("""
            SELECT states, alphabet FROM finite_automata WHERE id = %s
            """, (fa_id,))
            fa_info = cur.fetchone()
            if not fa_info:
                return
            
            states, alphabet = fa_info
            
            # Get all transitions
            cur.execute("""
            SELECT from_state, input_symbol, to_state
            FROM fa_transitions
            WHERE fa_id = %s
            ORDER BY from_state, input_symbol
            """, (fa_id,))
            
            # Build transition dictionary
            trans_dict = defaultdict(lambda: defaultdict(list))
            for from_state, symbol, to_state in cur.fetchall():
                trans_dict[from_state][symbol].append(to_state)
            
            # Display as table
            st.subheader("Transition Table")
            
            # Create header
            cols = st.columns(len(alphabet) + 1)
            with cols[0]:
                st.write("State \\ Symbol")
            for i, symbol in enumerate(alphabet):
                with cols[i+1]:
                    st.write(symbol)
            
            # Create rows
            for state in states:
                cols = st.columns(len(alphabet) + 1)
                with cols[0]:
                    st.write(f"**{state}**")
                for i, symbol in enumerate(alphabet):
                    with cols[i+1]:
                        if symbol in trans_dict[state]:
                            st.write(", ".join(trans_dict[state][symbol]))
                        else:
                            st.write("-")
            
        except Exception as e:
            st.error(f"Database error: {str(e)}")
        finally:
            if conn:
                conn.close()