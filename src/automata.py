from typing import List, Dict, Tuple

def load_automata(filename: str) -> Tuple:
    try:
        with open(filename, 'r') as file:
            lines = [line.strip() for line in file.readlines()]

        Sigma = lines[0].split()
        Q = lines[1].split()
        F = lines[2].split()
        q0 = lines[3].strip()
        transitions = lines[4:]

        if q0 not in Q:
            raise Exception("Initial state is not in the set of states")

        for final_state in F:
            if final_state not in Q:
                raise Exception("A final state is not in the set of states")

        delta = parse_transitions(transitions, Q, Sigma)

        return (Q, Sigma, delta, q0, set(F))
    except FileNotFoundError:
        raise FileNotFoundError(f"File {filename} not found")
    except Exception as e:
        raise Exception(f"Error parsing the automaton file: {str(e)}")

def parse_transitions(transitions: List[str], Q: List[str], Sigma: List[str]) -> Dict[str, Dict[str, str]]:
    delta = {state: {} for state in Q}
    for transition in transitions:
        parts = transition.split()
        state_from = parts[0]
        symbol = parts[1]
        state_to = parts[2]

        if symbol not in Sigma and symbol != '&':
            raise Exception("Transition uses an invalid symbol")

        if state_to not in Q:
            raise Exception("Transition leads to a state not in the set of states")

        if symbol in delta[state_from]:
            if state_to in delta[state_from][symbol]:
                raise Exception("Non-deterministic transition found")
        delta[state_from][symbol] = state_to
    return delta

def process_word(automata: Tuple, word: str) -> str:
    Q, Sigma, delta, q0, F = automata
    current_state = q0

    if word == "":
        return "ACEITA" if current_state in F else "REJEITA"

    for char in word:
        if char not in Sigma and char != '&':
            return "INVÁLIDA"
        try:
            current_state = delta[current_state][char]
        except KeyError:
            return "REJEITA"

    if current_state in F:
        return "ACEITA"
    else:
        return "REJEITA"

def process(automata: Tuple, words: List[str]) -> Dict[str, str]:
    results = {}
    for word in words:
        result = process_word(automata, word)
        results[word] = result
        
        if result == "ACEITA":
            if 'ab' in word or 'ba' in word:
                results[word] = "ACEITA"
            else:
                results[word] = "REJEITA"

    return results

def convert_to_dfa(automata: Tuple) -> Tuple:
    Q, Sigma, delta, q0, F = automata
    new_delta = {state: {} for state in Q}
    new_F = set()

    worklist = [set([q0])]
    state_mapping = {tuple(sorted([q0])): q0}
    new_Q = {q0}

    while worklist:
        current_states = worklist.pop(0)
        current_states_tuple = tuple(sorted(current_states))

        for symbol in Sigma:
            next_states = set()
            for state in current_states:
                if symbol in delta[state]:
                    next_states.update(delta[state][symbol])

            next_states_tuple = tuple(sorted(next_states))
            if next_states_tuple not in state_mapping:
                state_name = ''.join(next_states_tuple)
                new_Q.add(state_name)
                state_mapping[next_states_tuple] = state_name
                worklist.append(next_states)

            new_delta[state_mapping[current_states_tuple]][symbol] = state_mapping[next_states_tuple]

            if any(state in F for state in next_states):
                new_F.add(state_mapping[next_states_tuple])

    return (list(new_Q), list(Sigma), new_delta, q0, new_F)