from fa_classes import FAManager
from app import FAApp
import streamlit as st

def check():
    manager = FAManager()
    st.header("Define type of Finite Automata")
    fa_name = st.text_input("Enter your Finite Automata name:")
    fa = manager.load_fa(fa_name)
    if fa:
        if (fa.is_dfa()):
            st.success(f"Type of '{fa_name}' is a DFA ")
        else:
            st.success(f"Type of '{fa_name}' is an NFA ")
    else:
        st.warning(f"No FA found with name '{fa_name}'")
