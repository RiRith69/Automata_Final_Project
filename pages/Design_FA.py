# work


# app.py
import sys
import os

# Get absolute path to project root and add to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import streamlit as st
# from components.Temp_storage import FiniteAutomaton
# from pages.DFA_NFA import check


from components.Fa_model import FiniteAutomaton
from components.FA_database import FADatabaseHandler

class FAApp:
    def __init__(self):
        st.set_page_config(page_title="FA Designer", layout="wide")
        st.title("⚙️ Finite Automaton Designer")

        self.fa_db = FADatabaseHandler()
        self.fa = None

    def define_components(self):
        st.header("1. Define FA Components")
        self.fa_name = st.text_input("Name your FA:")
        self.fa_type = None
        states = st.text_input("Enter states (e.g., q0,q1,q2):")
        alphabet = st.text_input("Enter alphabet (e.g., a,b,ε):")

        if self.fa_name and states and alphabet:
            self.state_list = [s.strip() for s in states.split(",") if s.strip()]
            self.alphabet_list = [a.strip() for a in alphabet.split(",") if a.strip()]

            if self.state_list and self.alphabet_list:
                self.start_state = st.selectbox("Start State:", self.state_list)
                self.final_states = st.multiselect("Final States:", self.state_list)
                return True
            else:
                st.warning("Please enter at least one state and one alphabet symbol.")
        else:
            st.info("Please provide FA name, states, and alphabet to proceed.")
        return False

    def define_transitions(self):
        st.subheader("2. Define Transitions")
        transitions = {}

        for state in self.state_list:
            transitions[state] = {}
            for symbol in self.alphabet_list:
                key = f"{state}_{symbol}"
                selected = st.multiselect(f"δ({state}, {symbol}) =", self.state_list, key=key)
                transitions[state][symbol] = selected

        self.fa = FiniteAutomaton(
            self.fa_name,
            self.fa_type,
            self.state_list,
            self.alphabet_list,
            self.start_state,
            self.final_states,
            transitions
        )

    def display_summary(self):
        st.subheader("3. FA Summary")
        st.text(self.fa.display_FA())

        if st.button("💾 Save FA"):
            user_id = 1  # Replace with real user ID
            fa_id = self.fa_db.save_fa(self.fa, user_id)
            if fa_id:
                self.fa_db.save_transitions(fa_id, self.fa.transitions)
                st.success(f"FA '{self.fa_name}' saved successfully!")
            else:
                st.error("Failed to save FA.")

    def run(self):
        if self.define_components():
            self.define_transitions()
            self.display_summary()


if __name__ == "__main__":
    app = FAApp()
    app.run()
