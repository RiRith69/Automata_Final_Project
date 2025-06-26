from collections import defaultdict, deque
from .FA_database import FADatabaseHandler

def stringify_state(state):
    """Handle both string states and set-like states"""
    if not state:
        return "∅"
    if isinstance(state, (set, frozenset)):
        return "{" + ",".join(sorted(str(s) for s in state)) + "}"
    return str(state)

def stringify_states(states):
    """Handle both single states and collections"""
    if isinstance(states, (set, frozenset, list)):
        return [stringify_state(s) for s in states]
    return [stringify_state(states)]

class FiniteAutomaton:
    def __init__(self, name, states, alphabet, start_state, final_states, transitions, fa_type):
        self.name = name
        self.fa_type = fa_type
        self.states = states
        self.alphabet = alphabet
        self.start_state = start_state
        self.final_states = final_states
        self.transitions = transitions
        for state in self.transitions:
            for symbol in self.transitions[state]:
                fixed = []
                for dest in self.transitions[state][symbol]:
                    if isinstance(dest, list):
                        fixed.extend(dest)  # flatten one level
                        self.transitions[state][symbol] = fixed
    def save_to_db(self, user_id):
        return FADatabaseHandler().save_fa(self, user_id)

    @classmethod
    def load_from_db(cls, fa_name):
        fa_data = FADatabaseHandler().load_fa_info(fa_name)
        if fa_data:
            return cls(
                name=fa_data['name'],
                states=fa_data['states'],
                alphabet=fa_data['alphabet'],
                start_state=fa_data['start_state'],
                final_states=fa_data['final_states'],
                transitions=fa_data['transitions'],
                fa_type=fa_data['type']
            )
        return None

    def is_dfa(self):
        for state in self.states:
            for symbol in self.alphabet:
                if symbol not in self.transitions.get(state, {}):
                    return False
                if len(self.transitions[state][symbol]) != 1:
                    return False
            for symbol in self.transitions.get(state, {}):
                if symbol == '' or symbol.lower() == 'e':
                    return False
        return True
    def epsilon_closure(self, states):
        closure = set(states)
        queue = deque(states)
        
        while queue:
            state = queue.popleft()
            # Check for epsilon transitions (represented by 'ε' or '')
            epsilon_transitions = self.transitions.get(state, {}).get('', []) + self.transitions.get(state, {}).get('ε', [])
            
            for next_state in epsilon_transitions:
                if next_state not in closure:
                    closure.add(next_state)
                    queue.append(next_state)
        
        return frozenset(closure)
    
    def test_fa(self, input_string):
        current_states = {self.start_state}
        if self.fa_type == 'NFA':
                current_states = self.epsilon_closure({self.start_state.strip()})
        
        for symbol in input_string:
            if symbol not in self.alphabet :
                return False
            next_states = set()
            for state in current_states:
                reachable_states = self.transitions.get(state, {}).get(symbol, [])
                for target in reachable_states :
                    next_states.add(target)
                
            if not next_states:
                return False

            if fa.fa_type == 'NFA' :
                current_states = self.epsilon_closure(next_states)
            else :
                current_states = next_states
        
        return any(state in self.final_states for state in current_states)

    
    def convertor(self):
        # Initialize with epsilon closure of start state
        if self.fa_type != "NFA" :
            return
        try :
            dfa_start = self.epsilon_closure({self.start_state})
            dfa_states = {dfa_start}
            dfa_final = set()
            queue = deque([dfa_start])
            
            dfa_transitions = defaultdict(dict)
            # Process each DFA state (subset of NFA states)
            while queue:
                current_dfa_state = queue.popleft()

                # Check if this DFA state is accepting
                if any(state in self.final_states for state in current_dfa_state):
                    dfa_final.add(current_dfa_state)

                # Compute transitions for each symbol in the alphabet
                for symbol in self.alphabet:
                    next_states = set()
                    for nfa_state in current_dfa_state:
                        # Get all transitions for this NFA state and symbol
                        next_states.update(self.transitions.get(nfa_state, {}).get(symbol, []))
                    
                    # Take ε-closure of the result (if there were ε-transitions)
                    next_dfa_state = self.epsilon_closure(frozenset(next_states)) if next_states else frozenset()

                    if next_dfa_state:  # Only add if transitions exist
                        dfa_transitions[current_dfa_state][symbol] = next_dfa_state
                        if next_dfa_state not in dfa_states:
                            dfa_states.add(next_dfa_state)
                            queue.append(next_dfa_state)

            state_mapping = {
                state: f"p{i}"  
                for i, state in enumerate(dfa_transitions.keys())
            }

            # Rename transitions
            renamed_transitions = {
                state_mapping[old_state]: {
                    symbol: state_mapping[new_state]
                    for symbol, new_state in transitions.items()
                }
                for old_state, transitions in dfa_transitions.items()
            }

            # Rename start state
            renamed_start = state_mapping[dfa_start]

            # Rename final states (convert set to list)
            renamed_final = [
                state_mapping[state]
                for state in dfa_transitions
                if any(q in self.final_states for q in state)
            ]

            # Convert all sets to lists
            return {
                'name': self.name + " DFA",
                'fa_type': "DFA",
                'states': list(state_mapping.values()),  # Convert set to list
                'alphabet': list(self.alphabet),  # Convert set to list
                'start_state': renamed_start,
                'final_states': renamed_final,  # Already converted to list
                'transitions': renamed_transitions
            }
        except Exception as e :
            print(e)

    def minimize_dfa(self):
    # Convert all states to strings if they aren't already
        def stringify_state(state):
            if isinstance(state, (list, set, frozenset)):
                return ''.join(sorted(state))
            return str(state)
        # Convert all components to use string states
        dfa_states = [stringify_state(s) for s in self.states]
        dfa_start = stringify_state(self.start_state)
        dfa_final = [stringify_state(s) for s in self.final_states]
        
        # Convert transitions to use string states
        dfa_transitions = {}
        for state in self.transitions:
            str_state = stringify_state(state)
            dfa_transitions[str_state] = {}
            for symbol in self.transitions[state]:
                dfa_transitions[str_state][symbol] = stringify_state(self.transitions[state][symbol])
        
        # Initial partition: final and non-final states
        P = [set(dfa_final), set(dfa_states) - set(dfa_final)]
        W = [set(dfa_final), set(dfa_states) - set(dfa_final)]
        
        while W:
            A = W.pop(0)
            
            for c in self.alphabet:
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
            for symbol in self.alphabet:
                next_state = dfa_transitions[representative][symbol]
                next_partition = state_to_partition[next_state]
                new_transitions[new_state][symbol] = partition_to_new_state[frozenset(next_partition)]
        
        return {
            'name': f"{self.name} Minimized",
            'fa_type' : self.fa_type,
            'states': new_states,
            'alphabet': self.alphabet,
            'transitions': new_transitions,
            'start_state': new_start_state,
            'final_states': new_final_states
        }
            

    def display_FA(self):
        if self.transitions is None:
            return "**Error**: Transitions are not defined!"
        if self.states is None:
            return "**Error**: States are not defined!"
        if self.alphabet is None:
            return "**Error**: Alphabet is not defined!"
        if self.start_state is None:
            return "**Error**: Start state is not defined!"
        if self.final_states is None:
            return "**Error**: Final states are not defined!"
        output = f"**FA Name**: {self.name}\n"
        output += f"**FA Type**: {self.fa_type}\n"
        output += f"**States**: {', '.join(stringify_state(s) for s in self.states)}\n"
        output += f"**Alphabet**: {', '.join(self.alphabet)}\n"
        output += f"**Start State**: {stringify_state(self.start_state)}\n"
        output += f"**Final States**: {', '.join(stringify_state(s) for s in self.final_states)}\n"
        output += "**Transitions**:\n"
        for state in sorted(self.transitions):
            for symbol in sorted(self.transitions[state]):
                to_states = str(self.transitions.get(state, {}).get(symbol, []))
                to_state_str = to_states.replace("[", "").replace("]", " ").replace("'", "")
                output += f"\t{stringify_state(state)} --{symbol}--> {stringify_state(to_state_str)}\n"
        return output
    # In Fa_model.py
    def show_transition_table(self):
        if hasattr(self, 'id'):
            FADatabaseHandler().show_transition_table(self)
        else:
            # Fallback display if not saved to DB
            print("Transition table (not in DB):")
            for state in sorted(self.transitions):
                for symbol in sorted(self.transitions[state]):
                    print(f"δ({state}, {symbol}) = {self.transitions[state][symbol]}")
        

# fa_triple_ones = FiniteAutomaton(
#     name='Detect "111"',
#     fa_type= 'DFA',
#     states=['start', 'one', 'two', 'three'],
#     alphabet=['0', '1'],
#     start_state='start',
#     final_states=['three'],
#     transitions=[
#         ['start', '1', 'one'],
#         ['start', '0', 'start'],
#         ['one', '1', 'two'],
#         ['one', '0', 'start'],
#         ['two', '1', 'three'],
#         ['two', '0', 'start'],
#         ['three', '0', 'three'],
#         ['three', '1', 'three']
#     ]
# )

# Create a new FA
fa = FiniteAutomaton(
    name="Test FA",
    states=["q0", "q1"],
    alphabet=["a", "b"],
    start_state="q0",
    final_states=["q1"],
    transitions={
        "q0": {"a": ["q1"], "b": ["q0"]},
        "q1": {"a": ["q1"], "b": ["q0"]}
    },
    fa_type="DFA"
)