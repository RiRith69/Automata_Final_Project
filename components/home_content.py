import streamlit as st

def show_home():

    # Space between title and buttons
    st.markdown("")

    # Centered column layout
    col1, col2, col3 = st.columns(3)

    with col2:
        if st.button("🎨 Design Finite Automata", use_container_width=True) :
            st.switch_page("pages/Design_FA.py")
        
        if st.button("🔍 Check type of FA", use_container_width=True) :
            st.switch_page("pages/Check_FA.py")

        if st.button("🧪 Test FA wtih a string", use_container_width=True) :
            st.switch_page("pages/Test_FA.py")

        if st.button("🔁 Convert NFA to DFA", use_container_width=True) :
            st.switch_page("pages/Convert_FA.py")

        if st.button("🔽 Minimize DFA", use_container_width=True) :
            st.switch_page("pages/Minimize_DFA")
