import sys
import os

# Get absolute path to project root and add to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import streamlit as st

from components.FA_database import FADatabaseHandler
from components.Fa_model import FiniteAutomaton
from components.is_login import is_logged_in

st.set_page_config(page_title="DFA Perfictionist", layout="wide")
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

    fa = FiniteAutomaton.load_from_db(selected_fa)
    
    if fa.fa_type == "DFA" :

        new_dict = fa.minimize_dfa()
        try:
            required_keys = {'name', 'fa_type', 'states', 'alphabet', 'start_state', 'final_states', 'transitions'}
            if not required_keys.issubset(new_dict.keys()):
                st.error("Returned DFA dict is missing required fields.")
            else:
                try :
                    st.session_state.new_dfa = FiniteAutomaton(**new_dict)
                    st.subheader("DFA Minimized Summary :")
                    st.code(st.session_state.new_dfa.display_FA(), language='markdown')
                except Exception as e :
                    st.error(f"Error at : {e}")
        except Exception as e:
            st.error(f"❌ Conversion failed: {e}")
        # Button to convert NFA to DFA
        if st.button("Save new DFA"):

            if not hasattr(st.session_state, 'new_dfa'):
                st.error("No DFA created yet!")
                st.stop()
            
            try:
                # Save to database
                fa_id = st.session_state.new_dfa.save_to_db(st.session_state.user_id)
                
                if fa_id:
                    st.success(f"💾 DFA saved successfully with ID: {fa_id}")
                    st.balloons()  
                else:
                    st.error("No ID returned from database")
                    
            except Exception as e:
                st.error(f"❌ Saving failed: {str(e)}")
                # For debugging:
                import traceback
                st.text(traceback.format_exc())
    else :
        st.warning("Your FA is NFA! Please choose a DFA to minimize.")
if __name__ == "__main__":
    main()