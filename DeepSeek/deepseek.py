import streamlit as st
import psycopg2
import json
from itertools import chain, product
from collections import defaultdict, deque

# Database connection setup
def get_db_connection():
    return psycopg2.connect(
        host="localhost",
        database="finite_automata",
        user="team_leader",
        password="TL0123"
    )
# Initialize database tables
def init_db():
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Create FA table if not exists
    cur.execute("""
    CREATE TABLE IF NOT EXISTS finite_automata (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        description TEXT,
        states TEXT[] NOT NULL,
        alphabet TEXT[] NOT NULL,
        transitions JSONB NOT NULL,
        start_state TEXT NOT NULL,
        final_states TEXT[] NOT NULL,
        type VARCHAR(3) NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    # Create test cases table if not exists
    cur.execute("""
    CREATE TABLE IF NOT EXISTS test_cases (
        id SERIAL PRIMARY KEY,
        fa_id INTEGER REFERENCES finite_automata(id),
        input_string TEXT NOT NULL,
        expected_result BOOLEAN NOT NULL,
        actual_result BOOLEAN,
        passed BOOLEAN,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    conn.commit()
    cur.close()
    conn.close()

# Function to save FA to database
def save_fa_to_db(name, description, states, alphabet, transitions, start_state, final_states, fa_type):
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Convert transitions dictionary to JSON string
        transitions_json = json.dumps(transitions)
        
        cur.execute("""
        INSERT INTO finite_automata (name, description, states, alphabet, transitions, start_state, final_states, type)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING id
        """, (name, description, states, alphabet, transitions_json, start_state, final_states, fa_type))
        
        fa_id = cur.fetchone()[0]
        conn.commit()
        return fa_id
    except Exception as e:
        st.error(f"Database error: {str(e)}")
        return None
    finally:
        if conn:
            conn.close()

# Function to load FA from database
def load_fa_from_db(fa_id):
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute("""
        SELECT id, name, description, states, alphabet, 
               transitions::text, start_state, final_states, type
        FROM finite_automata WHERE id = %s
        """, (fa_id,))
        
        fa_data = cur.fetchone()
        
        if fa_data:
            # Convert JSON string back to dictionary
            transitions = json.loads(fa_data[5])
            return {
                'id': fa_data[0],
                'name': fa_data[1],
                'description': fa_data[2],
                'states': fa_data[3],
                'alphabet': fa_data[4],
                'transitions': transitions,
                'start_state': fa_data[6],
                'final_states': fa_data[7],
                'type': fa_data[8]
            }
        return None
    except Exception as e:
        st.error(f"Database error: {str(e)}")
        return None
    finally:
        if conn:
            conn.close()

# Function to check if FA is DFA or NFA
def check_fa_type(transitions, alphabet):
    for state, transitions_for_state in transitions.items():
        for symbol in alphabet:
            next_states = transitions_for_state.get(symbol, [])
            if len(next_states) > 1:
                return "NFA"
            if symbol not in transitions_for_state:
                return "NFA"  # Missing transition
    return "DFA"

# Function to get epsilon closure for NFA
def epsilon_closure(states, transitions):
    closure = set(states)
    queue = deque(states)
    
    while queue:
        state = queue.popleft()
        # Check for epsilon transitions (represented by 'ε' or '')
        epsilon_transitions = transitions.get(state, {}).get('', []) + transitions.get(state, {}).get('ε', [])
        
        for next_state in epsilon_transitions:
            if next_state not in closure:
                closure.add(next_state)
                queue.append(next_state)
    
    return frozenset(closure)

# Function to convert NFA to DFA
def nfa_to_dfa(nfa_states, alphabet, nfa_transitions, nfa_start, nfa_final):
    # Initialize with epsilon closure of start state
    dfa_start = epsilon_closure([nfa_start], nfa_transitions)
    dfa_states = {dfa_start}
    dfa_transitions = {}
    dfa_final = set()
    queue = deque([dfa_start])
    
    # Check if any state in the initial closure is final
    if any(state in nfa_final for state in dfa_start):
        dfa_final.add(dfa_start)
    
    while queue:
        current_dfa_state = queue.popleft()
        
        for symbol in alphabet:
            if symbol == '' or symbol == 'ε':
                continue  # Skip epsilon in DFA construction
                
            # Find all reachable states through this symbol
            next_states = set()
            for nfa_state in current_dfa_state:
                next_states.update(nfa_transitions.get(nfa_state, {}).get(symbol, []))
            
            if not next_states:
                continue
                
            # Get epsilon closure of these states
            new_dfa_state = epsilon_closure(next_states, nfa_transitions)
            
            if new_dfa_state not in dfa_states:
                dfa_states.add(new_dfa_state)
                queue.append(new_dfa_state)
                
                # Check if any state in the new DFA state is final
                if any(state in nfa_final for state in new_dfa_state):
                    dfa_final.add(new_dfa_state)
            
            # Add to transitions
            if current_dfa_state not in dfa_transitions:
                dfa_transitions[current_dfa_state] = {}
            dfa_transitions[current_dfa_state][symbol] = new_dfa_state
    
    # Convert frozenset states to readable names (e.g., {q0,q1} -> "q0q1")
    state_mapping = {}
    for i, state in enumerate(dfa_states):
        state_name = ''.join(sorted(state))
        state_mapping[state] = f"q{i}"
    
    # Create new DFA components with readable names
    readable_dfa_states = [state_mapping[state] for state in dfa_states]
    readable_dfa_start = state_mapping[dfa_start]
    readable_dfa_final = [state_mapping[state] for state in dfa_final]
    readable_dfa_transitions = {}
    
    for state in dfa_transitions:
        readable_state = state_mapping[state]
        readable_dfa_transitions[readable_state] = {}
        for symbol in dfa_transitions[state]:
            readable_dfa_transitions[readable_state][symbol] = state_mapping[dfa_transitions[state][symbol]]
    
    return {
        'states': readable_dfa_states,
        'alphabet': [sym for sym in alphabet if sym not in ('', 'ε')],
        'transitions': readable_dfa_transitions,
        'start_state': readable_dfa_start,
        'final_states': readable_dfa_final
    }

# Function to test a string on FA
def test_fa(fa, input_string):
    current_states = {fa['start_state']}
    
    # For NFA, we need to consider epsilon closures
    if fa['type'] == 'NFA':
        current_states = epsilon_closure(current_states, fa['transitions'])
    
    for symbol in input_string:
        next_states = set()
        for state in current_states:
            next_states.update(fa['transitions'].get(state, {}).get(symbol, []))
        
        if not next_states:
            return False
        
        if fa['type'] == 'NFA':
            current_states = epsilon_closure(next_states, fa['transitions'])
        else:
            current_states = next_states
    
    return any(state in fa['final_states'] for state in current_states)

# Function to minimize DFA using Moore's algorithm
def minimize_dfa(dfa):
    # Convert all states to strings if they aren't already
    def stringify_state(state):
        if isinstance(state, (list, set, frozenset)):
            return ''.join(sorted(state))
        return str(state)

    # Convert all components to use string states
    dfa_states = [stringify_state(s) for s in dfa['states']]
    dfa_start = stringify_state(dfa['start_state'])
    dfa_final = [stringify_state(s) for s in dfa['final_states']]
    
    # Convert transitions to use string states
    dfa_transitions = {}
    for state in dfa['transitions']:
        str_state = stringify_state(state)
        dfa_transitions[str_state] = {}
        for symbol in dfa['transitions'][state]:
            dfa_transitions[str_state][symbol] = stringify_state(dfa['transitions'][state][symbol])
    
    # Initial partition: final and non-final states
    P = [set(dfa_final), set(dfa_states) - set(dfa_final)]
    W = [set(dfa_final), set(dfa_states) - set(dfa_final)]
    
    while W:
        A = W.pop(0)
        
        for c in dfa['alphabet']:
            X = set()
            # Find all states that transition into A on c
            for state in dfa_states:
                if dfa_transitions.get(state, {}).get(c, None) in A:
                    X.add(state)
            
            # Refine each partition with X
            new_P = []
            for Y in P:
                intersect = Y & X
                difference = Y - X
                
                if intersect and difference:
                    new_P.append(intersect)
                    new_P.append(difference)
                    
                    if Y in W:
                        W.remove(Y)
                        W.append(intersect)
                        W.append(difference)
                    else:
                        if len(intersect) <= len(difference):
                            W.append(intersect)
                        else:
                            W.append(difference)
                else:
                    new_P.append(Y)
            
            P = new_P
    
    # Create new minimized DFA
    state_to_partition = {}
    for partition in P:
        for state in partition:
            state_to_partition[state] = partition
    
    # Create new states (one for each partition)
    new_states = []
    new_start_state = None
    new_final_states = []
    partition_to_new_state = {}
    
    for i, partition in enumerate(P):
        new_state = f"m{i}"
        partition_to_new_state[frozenset(partition)] = new_state
        new_states.append(new_state)
        
        # Check if partition contains the original start state
        if dfa_start in partition:
            new_start_state = new_state
        
        # Check if partition contains any final states
        if any(state in dfa_final for state in partition):
            new_final_states.append(new_state)
    
    # Create new transitions
    new_transitions = {}
    for partition in P:
        representative = next(iter(partition))
        new_state = partition_to_new_state[frozenset(partition)]
        
        new_transitions[new_state] = {}
        for symbol in dfa['alphabet']:
            next_state = dfa_transitions[representative][symbol]
            next_partition = state_to_partition[next_state]
            new_transitions[new_state][symbol] = partition_to_new_state[frozenset(next_partition)]
    
    return {
        'states': new_states,
        'alphabet': dfa['alphabet'],
        'transitions': new_transitions,
        'start_state': new_start_state,
        'final_states': new_final_states
    }
# Streamlit UI
def main():
    st.title("Finite Automata Project")
    st.write("Design, analyze, and test Finite Automata (DFA/NFA)")
    
    # Initialize database
    init_db()
    
    # Sidebar navigation
    menu = ["Design FA", "Check FA Type", "Convert NFA to DFA", "Test FA", "Minimize DFA"]
    choice = st.sidebar.selectbox("Select Function", menu)
    
    if choice == "Design FA":
        st.header("Design a Finite Automaton")
        
        name = st.text_input("Name your FA")
        description = st.text_area("Description")
        
        states_input = st.text_input("States (comma separated)", "q0,q1,q2")
        states = [s.strip() for s in states_input.split(",")]
        
        alphabet_input = st.text_input("Alphabet (comma separated)", "a,b")
        alphabet = [a.strip() for a in alphabet_input.split(",")]
        
        st.subheader("Transitions")
        transitions = {}
        for state in states:
            transitions[state] = {}
            st.markdown(f"**State {state}**")
            cols = st.columns(len(alphabet) + 1)  # +1 for epsilon
            
            for i, symbol in enumerate(alphabet):
                with cols[i]:
                    next_states = st.text_input(
                        f"On '{symbol}' goes to (comma separated)",
                        key=f"trans_{state}_{symbol}"
                    )
                    if next_states.strip():
                        transitions[state][symbol] = [s.strip() for s in next_states.split(",")]
            
            # Epsilon transition
            with cols[-1]:
                epsilon_states = st.text_input(
                    "On ε goes to (comma separated)",
                    key=f"trans_{state}_epsilon"
                )
                if epsilon_states.strip():
                    transitions[state]['ε'] = [s.strip() for s in epsilon_states.split(",")]
        
        start_state = st.selectbox("Start State", states)
        final_states = st.multiselect("Final States", states)
        
        if st.button("Save FA"):
            fa_type = check_fa_type(transitions, alphabet)
            fa_id = save_fa_to_db(
                name, description, states, alphabet, transitions, 
                start_state, final_states, fa_type
            )
            if fa_id:
                st.success(f"FA saved successfully with ID: {fa_id}")
                st.json({
                    "name": name,
                    "states": states,
                    "alphabet": alphabet,
                    "transitions": transitions,
                    "start_state": start_state,
                    "final_states": final_states,
                    "type": fa_type
                })

    elif choice == "Check FA Type":
        st.header("Check FA Type (DFA or NFA)")
        
        # Load FA from database
        conn = None
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute("SELECT id, name FROM finite_automata")
            fas = cur.fetchall()
            
            fa_options = {fa[0]: fa[1] for fa in fas}
            selected_fa = st.selectbox("Select FA", options=list(fa_options.keys()), 
                                     format_func=lambda x: f"{x} - {fa_options[x]}")
            
            if selected_fa and st.button("Check Type"):
                fa = load_fa_from_db(selected_fa)
                if fa:
                    st.write(f"**FA Name:** {fa['name']}")
                    st.write(f"**Type:** {fa['type']}")
                    st.json(fa['transitions'])
                else:
                    st.error("FA not found")
        except Exception as e:
            st.error(f"Database error: {str(e)}")
        finally:
            if conn:
                conn.close()
    
    elif choice == "Convert NFA to DFA":
        st.header("Convert NFA to DFA")
        
        # Load NFA from database
        conn = None
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute("SELECT id, name FROM finite_automata WHERE type = 'NFA'")
            nfas = cur.fetchall()
            
            nfa_options = {nfa[0]: nfa[1] for nfa in nfas}
            selected_nfa = st.selectbox("Select NFA", options=list(nfa_options.keys()), 
                                      format_func=lambda x: f"{x} - {nfa_options[x]}")
            
            if selected_nfa and st.button("Convert to DFA"):
                nfa = load_fa_from_db(selected_nfa)
                if nfa and nfa['type'] == 'NFA':
                    dfa = nfa_to_dfa(
                        nfa['states'], 
                        nfa['alphabet'], 
                        nfa['transitions'], 
                        nfa['start_state'], 
                        nfa['final_states']
                    )
                    
                    st.success("Conversion successful!")
                    st.subheader("Resulting DFA")
                    st.json(dfa)
                    
                    # Show transition table
                    st.subheader("Transition Table")
                    trans_table = []
                    for state in dfa['states']:
                        for symbol in dfa['alphabet']:
                            trans_table.append({
                                "State": state,
                                "Symbol": symbol,
                                "Next State": dfa['transitions'].get(state, {}).get(symbol, "-")
                            })
                    st.table(trans_table)
                else:
                    st.error("Selected FA is not an NFA or not found")
        except Exception as e:
            st.error(f"Database error: {str(e)}")
        finally:
            if conn:
                conn.close()
    
    elif choice == "Test FA":
        st.header("Test Strings on FA")
        
        # Load FA from database
        conn = None
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute("SELECT id, name FROM finite_automata")
            fas = cur.fetchall()
            
            fa_options = {fa[0]: fa[1] for fa in fas}
            selected_fa = st.selectbox("Select FA to test", options=list(fa_options.keys()), 
                                     format_func=lambda x: f"{x} - {fa_options[x]}")
            
            if selected_fa:
                fa = load_fa_from_db(selected_fa)
                if fa:
                    st.write(f"**Testing FA:** {fa['name']} ({fa['type']})")
                    
                    input_string = st.text_input("Input string to test")
                    if input_string and st.button("Test"):
                        result = test_fa(fa, input_string)
                        st.write(f"**Result:** {'Accepted' if result else 'Rejected'}")
                        
                        # Save test case
                        try:
                            conn2 = get_db_connection()
                            cur2 = conn2.cursor()
                            cur2.execute("""
                            INSERT INTO test_cases (fa_id, input_string, expected_result, actual_result, passed)
                            VALUES (%s, %s, %s, %s, %s)
                            """, (fa['id'], input_string, result, result, True))
                            conn2.commit()
                        except Exception as e:
                            st.error(f"Failed to save test case: {str(e)}")
                        finally:
                            if conn2:
                                conn2.close()
                else:
                    st.error("FA not found")
        except Exception as e:
            st.error(f"Database error: {str(e)}")
        finally:
            if conn:
                conn.close()
    
    elif choice == "Minimize DFA":
        st.header("Minimize DFA using Moore's Algorithm")
        
        # Load DFA from database
        conn = None
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute("SELECT id, name FROM finite_automata WHERE type = 'DFA'")
            dfas = cur.fetchall()
            
            dfa_options = {dfa[0]: dfa[1] for dfa in dfas}
            selected_dfa = st.selectbox("Select DFA to minimize", options=list(dfa_options.keys()), 
                                      format_func=lambda x: f"{x} - {dfa_options[x]}")
            
            if selected_dfa and st.button("Minimize DFA"):
                dfa = load_fa_from_db(selected_dfa)
                if dfa and dfa['type'] == 'DFA':
                    minimized_dfa = minimize_dfa(dfa)
                    
                    st.success("Minimization successful!")
                    st.subheader("Original DFA")
                    st.json({
                        "states": dfa['states'],
                        "alphabet": dfa['alphabet'],
                        "start_state": dfa['start_state'],
                        "final_states": dfa['final_states']
                    })
                    
                    st.subheader("Minimized DFA")
                    st.json(minimized_dfa)
                    
                    # Show transition table
                    st.subheader("Minimized Transition Table")
                    trans_table = []
                    for state in minimized_dfa['states']:
                        for symbol in minimized_dfa['alphabet']:
                            trans_table.append({
                                "State": state,
                                "Symbol": symbol,
                                "Next State": minimized_dfa['transitions'].get(state, {}).get(symbol, "-")
                            })
                    st.table(trans_table)
                else:
                    st.error("Selected FA is not a DFA or not found")
        except Exception as e:
            st.error(f"Database error: {str(e)}")
        finally:
            if conn:
                conn.close()

if __name__ == "__main__":
    main()