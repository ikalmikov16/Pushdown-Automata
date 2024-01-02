from tabulate import tabulate

class PDA:
    def __init__(self, states : set, alphabet : set, stack_alphabet : set, start_state : str,
                 final_state : str, transition_functions : dict):
        self.states = states
        self.alphabet = alphabet
        self.stack_alphabet = stack_alphabet
        self.start_state = start_state
        self.final_state = final_state
        self.transition_functions = transition_functions
        self.stack = []
        self.possible_functions = self.get_possible_functions(self.transition_functions)
    
    # Function to create hashmap to store possible functions from each State
    def get_possible_functions(self, t : dict) -> dict:
        # Initialize hashmap
        # state : [[input, stack], [input, stack]...]
        pf = {}
        for key in t:
            state = key[0]
            arr = [key[1], key[2]]
        
            if state not in pf:
                pf[state] = []
            pf[state].append(arr)
        
        return pf
    
    # Function to check if PDA accepts input String
    def accepts(self, input : str) -> bool:
        # Initialize Variables
        current_state = self.start_state
        self.stack = []

        # Mark String end with $
        input += "$"
        i = 0

        # table array for final results display
        table_array = [["State", "Unread Input", "Stack", "Delta Rule", "R Rule"],
                       [current_state, input, "", "-", "-"]]
        
        while True:
            # Initialize Variables
            skip_input = False
            read_stack = False
            # Store Transition functions key
            func_key = ()

            # Get list of possible functions from current state
            possible = self.possible_functions[current_state]

            # Determine Transition Function 
            func_key = self.get_function_key(current_state, possible, input[i])
            # If no possible functions
            if not func_key:
                self.display_table(table_array)
                return False
            # Modify skip_input and read_stack if necessary
            if func_key[1] is None:
                skip_input = True
            if func_key[2]:
                read_stack = True

            # Determine function result
            rule_num, current_state, next_stack = self.transition_functions[func_key]
            if next_stack:
                next_stack = reversed(list(next_stack))

            # Update input index
            if not skip_input:
                i += 1
            # Update Stack
            if read_stack:
                self.stack.pop()
                if next_stack:
                    self.stack.extend(next_stack)
            elif next_stack:
                self.stack.extend(next_stack)
            
            # Stack string for nicer display
            stack_string = "".join(self.stack)[1:]
            stack_string = stack_string[::-1]
            # Update Display Table
            if rule_num == "7":
                table_array.append([current_state, input[i:], 
                                    stack_string, rule_num, "a -> aSb"])
            elif rule_num == "8":
                table_array.append([current_state, input[i:], stack_string, 
                                    rule_num, "S -> e"])
            else:
                table_array.append([current_state, input[i:], stack_string, 
                                    rule_num, "-"])
            
            # If Final State is Reached 
            if current_state == self.final_state:
                self.display_table(table_array)
                return True
        return False 
    
    # Function to Determine Function from the current state
    def get_function_key(self, current_state : str, possible : list,
                          next_input : str) -> tuple:
        # Iterate thru possible functions from current state
        key = ()
        symbol = None
        read_stack = False

        for arr in possible:
            # Check input symbol
            # If input symbol not read
            if arr[0] is None:
                symbol = None
            # If input symbol matches function
            elif next_input == arr[0]:
                symbol = next_input
            # If input symbol does not match function
            else:
                continue
            
            # Check Stack
            # If Stack is not read
            if arr[1] is None:
                read_stack = False
            # If Stack top matches function
            elif self.stack and self.stack[-1] == arr[1]:
                read_stack = True
            # If Stack top does not match function
            else:
                continue
            
            # Function Key
            if not read_stack:
                key = (current_state, symbol, None)
            else:
                key = (current_state, symbol, self.stack[-1])
            break
        return key
    
    def display_table(self, table_array) -> None:
        print(tabulate(table_array, headers = "firstrow", colalign = ("right","left","right", "right","left"), tablefmt = "fancy_grid", showindex = True))
        pass