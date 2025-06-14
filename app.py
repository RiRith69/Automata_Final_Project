# app.py

import streamlit as st
from fa_classes import FiniteAutomaton, FAManager


class FAApp:
    def __init__(self):
        st.set_page_config(page_title="FA Designer", layout="wide")
        st.title("⚙️ Finite Automaton Designer")

        self.fa_manager = FAManager()
        self.fa = None

    def load_saved_fa(self):
        st.sidebar.header("📂 Load Saved FA")
        saved_fas = self.fa_manager.list_saved_fas()

        if saved_fas:
            selected_fa_name = st.sidebar.selectbox("Select an FA to load:", saved_fas)
            if st.sidebar.button("🔄 Load FA"):
                loaded_fa = self.fa_manager.load_fa(selected_fa_name)
                if loaded_fa:
                    st.sidebar.success(f"Loaded FA '{selected_fa_name}'")
                    st.json(loaded_fa.to_dict())
                else:
                    st.sidebar.error("Failed to load FA.")
        else:
            st.sidebar.info("No saved FAs found.")

    def define_components(self):
        st.header("1. Define FA Components")

        self.fa_name = st.text_input("Name your FA:")
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
            self.state_list,
            self.alphabet_list,
            self.start_state,
            self.final_states,
            transitions
        )

    def display_summary(self):
        st.subheader("3. FA Summary")
        st.json(self.fa.to_dict())

        if st.button("💾 Save FA to File"):
            self.fa_manager.save_fa(self.fa)
            st.success(f"FA '{self.fa_name}' saved successfully!")

    def run(self):
        self.load_saved_fa()
        if self.define_components():
            self.define_transitions()
            self.display_summary()


if __name__ == "__main__":
    app = FAApp()
    from DFA_NFA import check
    check()
    app.run()
