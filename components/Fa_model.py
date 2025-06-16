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

    def display_FA(self):
        output = f"FA Name: {self.name}\n"
        output += f"FA Type: {self.fa_type}\n"
        output += f"States: {', '.join(self.states)}\n"
        output += f"Alphabet: {', '.join(self.alphabet)}\n"
        output += f"Start State: {self.start_state}\n"
        output += f"Final States: {', '.join(self.final_states)}\n"
        output += "Transitions:\n"
        for state in self.transitions:
            for symbol in self.transitions[state]:
                to_states = self.transitions[state][symbol]
                output += f"  {state} --{symbol}--> {to_states}\n"
        return output
