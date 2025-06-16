# work

import sys
import os

# Get absolute path to project root and add to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import streamlit as st

from components.FA_database import FADatabaseHandler
from components.Fa_model import FiniteAutomaton

def main():
    st.title("🔍 FA Type Checker")
    st.markdown("Check if your FA is a **DFA** or **NFA** based on its transition function.")

    manager = FADatabaseHandler()
    fa_name = st.text_input("Enter your Finite Automata name:")

    if fa_name:
        fa_data = manager.load_fa_by_name(fa_name)
        if fa_data:
            try:
                fa = FiniteAutomaton(**fa_data)  # Requires fa_data to be a matching dict
                if fa.is_dfa():
                    st.success(f"The FA '{fa_name}' is a **DFA** ✅")
                else:
                    st.warning(f"The FA '{fa_name}' is an **NFA** ⚠️")
            except Exception as e:
                st.error(f"Error creating FA object: {e}")
        else:
            st.error(f"No FA found with the name '{fa_name}'")

if __name__ == "__main__":
    main()
