# work

import sys
import os

# Get absolute path to project root and add to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import streamlit as st

from components.FA_database import FADatabaseHandler
from components.Fa_model import FiniteAutomaton
from components.is_login import is_logged_in

st.set_page_config(page_title="FK Scout", layout="wide")
is_logged_in()

if st.session_state.get("logged_in"):
    user_id = st.session_state.user_id


def main():
    st.title("🔍 FA Type Checker")
    st.markdown("Check if your FA is a **DFA** or **NFA** based on its transition function.")

    manager = FADatabaseHandler()
    fa_names = manager.load_all_fa_names(st.session_state.username)

    if not fa_names:
        st.info("⚠️ You don't have any FA saved. Please design one first.")
        st.stop()

    fa_name_options = [fa[1] for fa in fa_names]
    selected_fa = st.selectbox("Select a Finite Automaton:", fa_name_options)

    fa = FiniteAutomaton.load_from_db(selected_fa)
    if fa:
        try:  # Requires fa_data to be a matching dict
            if fa.fa_type == "DFA":
                st.success(f"The FA '{fa.name}' is a **DFA** ✅")
            else:
                st.warning(f"The FA '{fa.name}' is an **NFA** ⚠️")
            # Show transition table
            st.subheader("Transition Table")
            trans_table = []
            for state in fa.states:
                for symbol in fa.alphabet:
                    to_states = str(fa.transitions.get(state, {}).get(symbol, []))
                    to_state_str = to_states.replace("[", "").replace("]", " ").replace("'", "")
                    
                    if state == fa.start_state :
                        trans_table.append({
                            "From State": '-->\t' + state,
                            "Symbol": symbol,
                            "To State": to_state_str
                        })
                    elif state in fa.final_states :
                        trans_table.append({
                            "From State": '*' + state,
                            "Symbol": symbol,
                            "To State": to_state_str
                        })
                    else :
                        trans_table.append({
                            "From State": state,
                            "Symbol": symbol,
                            "To State": to_state_str
                        })
            st.table(trans_table)
        except Exception as e:
            st.error(f"Error creating FA object: {e}")
    else:
        st.error(f"No FA found")

if __name__ == "__main__":
    main()
