# fa_classes.py

import json
import os

class FiniteAutomaton:
    def __init__(self, name, states, alphabet, start_state, final_states, transitions):
        self.name = name
        self.states = states
        self.alphabet = alphabet
        self.start_state = start_state
        self.final_states = final_states
        self.transitions = transitions

    def to_dict(self):
        return {
            "name": self.name,
            "states": self.states,
            "alphabet": self.alphabet,
            "start_state": self.start_state,
            "final_states": self.final_states,
            "transitions": self.transitions
        }

    @staticmethod
    def from_dict(data):
        return FiniteAutomaton(
            data["name"],
            data["states"],
            data["alphabet"],
            data["start_state"],
            data["final_states"],
            data["transitions"]
        )
    def is_dfa(self):
        for state in self.states:
            for symbol in self.alphabet:
                if symbol not in self.transitions.get(state, {}):
                    return False
                if len(self.transitions[state][symbol]) != 1:
                    return False
            for symbol in self.transitions.get(state, {}):
                if symbol == '' or symbol.lower() == 'ε':
                    return False
        return True


class FAManager:
    def __init__(self, save_path="data"):
        self.save_path = save_path
        os.makedirs(save_path, exist_ok=True)

    def save_fa(self, fa: FiniteAutomaton):
        filepath = os.path.join(self.save_path, f"{fa.name}.json")
        with open(filepath, "w") as f:
            json.dump(fa.to_dict(), f, indent=4)

    def load_fa(self, name):
        filepath = os.path.join(self.save_path, f"{name}.json")
        if os.path.exists(filepath):
            with open(filepath, "r") as f:
                data = json.load(f)
                return FiniteAutomaton.from_dict(data)
        return None
    
    def list_saved_fas(self):
        return [f.replace(".json", "") for f in os.listdir(self.save_path) if f.endswith(".json")]

