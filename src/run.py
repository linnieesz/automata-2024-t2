from automata import load_automata, process

automata = load_automata("examples\\01-simples.txt")

results = process(automata, ["aabb", "abab", "baba", "abc"])
print(results)
