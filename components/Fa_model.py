class FiniteAutomaton:
    def __init__(self, name, fa_type, states, alphabet, start_state, final_states, transitions):
        self.name = name
        self.states = states
        self.fa_type = fa_type
        self.alphabet = alphabet
        self.start_state = start_state
        self.final_states = final_states
        self.transitions = transitions

    def is_dfa(self):
        for state in self.states:
            for symbol in self.alphabet:
                if symbol not in self.transitions.get(state, {}):
                    return False
                if len(self.transitions[state][symbol]) != 1:
                    return False
            for symbol in self.transitions.get(state, {}):
                if symbol == '' or symbol.lower() == 'e' or symbol.lower() == 'ε':
                    return False
        return True
    
    def is_accepted_dfa(self, input_string) :
        current_state = self.start_state
        for symbol in input_string :
            found = False
            for tran in self.transitions :
                if tran[0] == current_state and tran[1] == symbol :
                    current_state = tran[2]
                    found = True
                    break
            if not found :
                return False
        return current_state in self.final_states
    
    def is_accepted_nfa(self, input_string) :
        def dfs(state, index):
        # Base case: if input is fully read
            if index == len(input_string):
                return state in self.final_states  # Accept if current state is final

            symbol = input_string[index]

            # Find all transitions from 'state' using the current symbol
            next_states = [
                t[2] for t in self.transitions
                if t[0] == state and t[1] == symbol
            ]

            # Try each next state (non-determinism)
            for next_state in next_states:
                if dfs(next_state, index + 1):  # Recursive check
                    return True  # Accept as soon as one path works

            return False  # No path accepted the string

        # Start DFS from start_state and character at index 0
        return dfs(self.start_state, 0)

    def display_FA(self):
        output = f"**FA Name**: {self.name}\n"
        output += f"**FA Type**: {self.fa_type}\n"
        output += f"**States**: {', '.join(self.states)}\n"
        output += f"**Alphabet**: {', '.join(self.alphabet)}\n"
        output += f"**Start State**: {self.start_state}\n"
        output += f"**Final States**: {', '.join(self.final_states)}\n"
        output += "**Transitions**:\n"
        for state in self.transitions:
            for symbol in self.transitions[state]:
                to_states = self.transitions[state][symbol]
                output += f"\t{state} --{symbol}--> {to_states}\n"
        return output
