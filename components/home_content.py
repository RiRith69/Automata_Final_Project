import streamlit as st

def show_home():

    # Space between title and buttons
    st.markdown("")

    # Centered column layout
    col1, col2, col3 = st.columns(3)

    with col2:
        if st.button("🎨 Design Finite Automata", use_container_width=True) :
            st.switch_page("Design FA")
        
        if st.button("🔍 Check type of FA", use_container_width=True) :

            st.switch_page("DFA NFA.py")
        st.button("🧪 Test FA wtih a string", use_container_width=True, key="test_btn", on_click=lambda: st.session_state.update(page="Test FA wtih a string"))
        st.button("🔁 Convert NFA to DFA", use_container_width=True, key="convert_btn", on_click=lambda: st.session_state.update(page="Convert NFA to DFA"))
        st.button("🔽 Minimize DFA", use_container_width=True, key="minimize_btn", on_click=lambda: st.session_state.update(page="Minimize DFA"))
