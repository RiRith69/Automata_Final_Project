import sys
import os
import streamlit as st
from components.Fa_model import FiniteAutomaton
from components.is_login import is_logged_in
from collections import defaultdict

# Configure the app
st.set_page_config(page_title="FA Designer", layout="wide")

class FAApp:
    def __init__(self):
        st.title("⚙️ Finite Automaton Designer")
        self.fa = None
        self.state_list = []
        self.alphabet_list = []

    def define_components(self):
        """Collect basic FA components from user"""
        st.header("1. Define FA Components")
        
        # Input fields with default values
        self.fa_name = st.text_input("Name your FA:")
        states = st.text_input("Enter states (comma separated. eg, q0, q1):")
        alphabet = st.text_input("Enter alphabet (comma separated. eg, 0, 1):")
        
        # Process inputs
        if self.fa_name and states and alphabet:
            self.state_list = [s.strip() for s in states.split(",") if s.strip()]
            self.alphabet_list = [a.strip() for a in alphabet.split(",") if a.strip()]

            if self.state_list and self.alphabet_list:
                self.start_state = st.selectbox("Start State:", self.state_list)
                self.final_states = st.multiselect("Final States:", self.state_list)
                return True
        
        st.warning("Please complete all fields to proceed")
        return False

    def define_transitions(self):
        """Collect transition function from user"""
        st.subheader("2. Define Transitions")
        st.markdown("**Note:** Use 'e' for epsilon transitions")
        
        transitions = defaultdict(lambda: defaultdict(list))
        has_epsilon = False
        
        # Add epsilon temporarily for transition definition
        full_alphabet = self.alphabet_list + ['e']
        
        # Create columns for each symbol
        cols = st.columns(len(full_alphabet))
        
        for state in self.state_list:
            with st.expander(f"**{state} Transitions**") :
                transitions[state] = {}
                cols = st.columns(len(full_alphabet))
                for i, symbol in enumerate(full_alphabet):
                    with cols[i]:
                        selected = st.multiselect(
                            f"δ({state}, {symbol})",
                            self.state_list,
                            key=f"trans_{state}_{symbol}"
                        )
                        if selected:
                            transitions[state][symbol] = selected
                            if symbol == 'e':
                                has_epsilon = True
        
        # Determine FA type
        is_dfa = True
        for state in self.state_list:
            for symbol in self.alphabet_list:  # Only check non-epsilon symbols
                if len(transitions[state].get(symbol, [])) != 1:
                    is_dfa = False
                    break
        
        self.fa_type = "DFA" if is_dfa and not has_epsilon else "NFA"
        
        # Create the FA instance
        try:
            self.fa = FiniteAutomaton(
                name=self.fa_name,
                states=self.state_list,
                alphabet=self.alphabet_list,  # Without epsilon
                start_state=self.start_state,
                final_states=self.final_states,
                transitions=dict(transitions),
                fa_type=self.fa_type
            )
            
            # Show FA type feedback
            if has_epsilon:
                st.warning("⚠️ This is an NFA (contains epsilon transitions)")
            elif not is_dfa:
                st.warning("⚠️ This is an NFA (non-deterministic transitions)")
            else:
                st.success("✓ This is a DFA")
                
            return True
            
        except Exception as e:
            st.error(f"Error creating FA: {str(e)}")
            return False

    def save_fa_to_db(self):
        """Handle database saving with proper error checking"""
        if not self.fa:
            st.error("No FA to save")
            return None
        
        try:
            # Ensure we have a valid user ID
            if not hasattr(st.session_state, 'user_id'):
                st.error("User not authenticated")
                return None
                
            fa_id = self.fa.save_to_db(st.session_state.user_id)
            if fa_id:
                st.success(f"FA '{self.fa.name}' saved successfully with ID: {fa_id}")
                return fa_id
            else:
                st.error("Failed to save FA (no ID returned)")
                return None
                
        except Exception as e:
            st.error(f"Database error: {str(e)}")
            return None

    def display_summary(self):
        """Display FA summary and handle saving"""
        st.subheader("3. FA Summary")
        
        if not self.fa:
            st.error("No FA to display")
            return
            
        # Display FA properties
        st.code(self.fa.display_FA(), language='markdown')
        # Save button
        if st.button("💾 Save FA"):
            self.save_fa_to_db()

    def run(self):
        """Main application flow"""
        if not st.session_state.get("logged_in"):
            st.error("⚠️ Please log in to access the FA Designer")
            return
            
        if self.define_components():
            if self.define_transitions():
                self.display_summary()

# Run the app
if __name__ == "__main__":
    is_logged_in()  # Check authentication
    app = FAApp()
    app.run()