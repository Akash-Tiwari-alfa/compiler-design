import tkinter as tk
from tkinter import messagebox, scrolledtext

class GrammarProcessor:
    def __init__(self, grammar):
        self.grammar = self.parse_grammar(grammar)
    
    def parse_grammar(self, grammar_text):
        grammar = {}
        for line in grammar_text.strip().split("\n"):
            if "->" in line:
                lhs, rhs = line.split("->")
                lhs = lhs.strip()
                rhs = [rule.strip() for rule in rhs.split("|")]
                grammar[lhs] = rhs
        print("Parsed Grammar:", grammar)  # Debugging Print
        return grammar
    
    def eliminate_left_recursion(self):
        new_grammar = {}
        for non_terminal in list(self.grammar.keys()):
            recursive = []
            non_recursive = []
            new_nt = non_terminal + "'"
            
            for rule in self.grammar[non_terminal]:
                if rule.startswith(non_terminal):  # Direct left recursion
                    recursive.append(rule[len(non_terminal):].strip() + " " + new_nt)
                else:
                    non_recursive.append(rule + " " + new_nt)

            if recursive:
                new_grammar[non_terminal] = non_recursive
                new_grammar[new_nt] = recursive + ["ε"]  # Adding epsilon for termination
            else:
                new_grammar[non_terminal] = self.grammar[non_terminal]
        
        print("Left Recursion Removed Grammar:", new_grammar)  # Debugging Print
        return new_grammar
    
    def left_factor(self):
        new_grammar = {}
        for non_terminal, rules in self.grammar.items():
            prefixes = {}
            for rule in rules:
                first_symbol = rule.split()[0]
                if first_symbol not in prefixes:
                    prefixes[first_symbol] = []
                prefixes[first_symbol].append(rule)
            
            if len(prefixes) == len(rules):
                new_grammar[non_terminal] = rules
            else:
                new_nt = non_terminal + "'"
                new_grammar[non_terminal] = [k + " " + new_nt for k in prefixes]
                new_grammar[new_nt] = [r.replace(k, "", 1).strip() or "ε" for k, v in prefixes.items() for r in v]
        
        print("Left Factored Grammar:", new_grammar)  # Debugging Print
        return new_grammar

def process_grammar(operation):
    grammar_text = grammar_input.get("1.0", tk.END).strip()
    print("User Input Grammar:", grammar_text)  # Debugging Print

    if not grammar_text:
        messagebox.showerror("Error", "Please enter a grammar.")
        return
    
    processor = GrammarProcessor(grammar_text)
    
    if operation == "recursion":
        result = processor.eliminate_left_recursion()
    elif operation == "factoring":
        result = processor.left_factor()
    else:
        return
    
    # Debugging: Ensure the result is correct before displaying
    print("Processed Grammar Output:", result)

    output_text.config(state=tk.NORMAL)  # Enable editing before inserting text
    output_text.delete("1.0", tk.END)  # Clear previous text

    for nt, rules in result.items():
        output_text.insert(tk.END, f"{nt} -> {' | '.join(rules)}\n")

    output_text.config(state=tk.DISABLED)  # Disable editing after inserting text

# GUI Setup
window = tk.Tk()
window.title("Grammar Processor")
window.geometry("600x500")

tk.Label(window, text="Enter Grammar:").pack()
grammar_input = scrolledtext.ScrolledText(window, width=70, height=10)
grammar_input.pack()

tk.Button(window, text="Eliminate Left Recursion", command=lambda: process_grammar("recursion")).pack(pady=5)
tk.Button(window, text="Left Factor", command=lambda: process_grammar("factoring")).pack(pady=5)

tk.Label(window, text="Output:").pack()
output_text = scrolledtext.ScrolledText(window, width=70, height=10, state=tk.DISABLED)
output_text.pack()

window.mainloop()
