from PDA import PDA

# Define PDA Variables
states = {"p, q, qa, qb, q$"}
alphabet = {"a", "b"}
stack_alphabet = {"a", "b", "S"}
start_state = "p"
final_state = "q$"
# Transition Rule format
# Key =   (current state, input read - if None don't read, 
#          top of stack - if None don't read)
# Value = (rule number, destionation state, stack actions:
#          string - push, None - pop or nothing)
transition_function = {
    ("p", "$", None)  : ("9", "q$", None),
    ("p", None, None) : ("1", "q", "SZ"),
    ("q", "a", None)  : ("2", "qa", None),
    ("qa", None, "a") : ("3", "q", None),
    ("q", "b", None)  : ("4", "qb", None),
    ("qb", None, "b") : ("5", "q", None),
    ("q", "$", "Z")   : ("6", "q$", None),
    ("qa", None, "S") : ("7", "qa", "aSb"),
    ("qb", None, "S") : ("8", "qb", None)
}

# Define PDA
dpda = PDA(states, alphabet, stack_alphabet, start_state, 
           final_state, transition_function)
print (dpda.accepts(""))

