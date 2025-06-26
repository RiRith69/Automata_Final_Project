import sys
import os

# Get absolute path to project root and add to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import streamlit as st

from components.FA_database import FADatabaseHandler
from components.Fa_model import FiniteAutomaton
from components.is_login import is_logged_in

st.set_page_config(page_title="FA Player", layout="wide")
is_logged_in()

if st.session_state.get("logged_in"):
    user_id = st.session_state.user_id


def main():
    st.title("🧪 FA String Tester")
    st.markdown("Check if your FA accept the input string or not.")

    manager = FADatabaseHandler()
    fa_names = manager.load_all_fa_names(st.session_state.username)

    if not fa_names:
        st.info("⚠️ You don't have any FA saved. Please design one first.")
        st.stop()

    fa_name_options = [fa[1] for fa in fa_names]
    selected_fa = st.selectbox("Select a Finite Automaton:", fa_name_options)


    test_string = st.text_input("Enter a string to test:")
    fa = FiniteAutomaton.load_from_db(selected_fa)
    if fa :
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
        
        if st.button("Test String") :
            if test_string == "" :
                st.warning("Please enter a string to test ⚠️")
            elif any(s not in fa.alphabet for s in test_string) :
                st.warning("Invalid string")
            else :
                checked = fa.test_fa(test_string)
                if checked :
                    st.success(f"The FA '{selected_fa}' is **accpet** input string ✅")
                else:
                    st.warning(f"The FA '{selected_fa}' is **reject** input string ⚠️")
    else:
        st.error(f"Invalid FA")

if __name__ == "__main__":
    main()