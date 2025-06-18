import sys
import os

# Get absolute path to project root and add to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import streamlit as st

from components.FA_database import FADatabaseHandler
from components.Fa_model import FiniteAutomaton
from components.is_login import is_logged_in

is_logged_in()

def main():
    st.title("🧪 FA String Tester")
    st.markdown("Check if your FA accept the input string or not.")

    manager = FADatabaseHandler()
    fa_names = manager.load_all_fa_names(st.session_state.username)

    if not fa_names:
        st.info("⚠️ You don't have any FA saved. Please design one first.")
        st.stop()

    fa_name_options = [fa[0] for fa in fa_names]
    selected_fa_name = st.selectbox("Select a Finite Automaton:", fa_name_options)

    fa_data = manager.load_fa_by_name(selected_fa_name)

    test_string = st.text_input("Enter a string to test:")

    fa = FiniteAutomaton(**fa_data)  # Requires fa_data to be a matching dict
    fa.display_FA()
    if st.button("Test String") :
        if test_string == "" :
            st.warning("Please enter a string to test ⚠️")
        else :
            fa.is_accepted_dfa(test_string)
            if fa.fa_type == "DFA":
                if fa.is_accepted_dfa(test_string) :
                    st.success(f"The FA '{selected_fa_name}' is **accpet** input string ✅")
                else:
                    st.warning(f"The FA '{selected_fa_name}' is **reject** input string ⚠️")
            else :
                if fa.is_accepted_nfa(test_string) :
                    st.success(f"The FA '{selected_fa_name}' is **accpet** input string ✅")
                else:
                    st.warning(f"The FA '{selected_fa_name}' is **reject** input string ⚠️")
    else:
        st.error(f"Invalid FA")

if __name__ == "__main__":
    main()