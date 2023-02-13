"""
calculator.py

This program creates registers with values and can make simple calculations on these values.
Takes input from user in the terminal.

Classes:
    - Calculator
    - Register

Methods:
    - run(): Runs the program and handles the input from the user.
    - store_lazy_evaluations(): Stores calculations between registers, these are calculated at print.

"""

class Calculator:
    """
    Calculator class

    Attributes:
        - register_list: List that holds all the registers
        - operation_list: List that holds all operations that are allowed, add, subtract, and multiply
        - stored_operations: List that holds all operations between registers, these are calculated when we print.

    Methods:
        - make_calculations: Checks which operation to make and if the input was valid, also stores calculation
          if the calculation is between two registers.
        - addition: Makes add operation
        - subtract: Makes subtract operation
        - multiply: Makes multiply operation
    """
    def __init__(self, register_list, operation_list, stored_operations):
        self.register_list = register_list
        self.stored_operations = stored_operations
        self.operation_list = operation_list

    def make_calculation(self, register, input):
        # Checks if the value is numeric and not a register
        if input[2].isdigit():
            # Make calculation and add new value to the register
            if input[1] == 'add':
                self.addition(register, input[2])
            elif input[1] == 'subtract':
                self.subtract(register, input[2])
            elif input[1] == 'multiply':
                self.multiply(register, input[2])
            else:
                print('Invalid operation, must be: add, subtract, or multiply')
        else:
            # Check that operation is valid
            if input[1] in self.operation_list:
                # Store operation for lazy evaluation since the value were not only digits
                store_lazy_evaluations(self, input, register)
            else:  
                print('Invalid operation, must be: add, subtract, or multiply')
        

    def addition(self, register, value):
        register.value = (register.value + int(value))
    
    def subtract(self, register, value):
        register.value  = (register.value - int(value))
    
    def multiply(self, register, value):
        register.value = (register.value * int(value))


class Register:
    """
    Register class

    Attributes:
        - name: name of the register
        - value: value of the register
    """
    def __init__(self, name, value):
        self.name = name
        self.value = value

def store_lazy_evaluations(calculator, input, reg):
    # Store register instead of name so we can access the value later
    input[0] = reg
    if input[2] not in calculator.register_list:
        reg2 = Register(input[2], 0)
        # Store register instead of name so we can access the value later
        input[2] = reg2
        calculator.register_list.append(reg2)
    else:
        for reg in calculator.register_list:
            if reg == input[2]:
                # Store register instead of name so we can access the value later
                input[2] = reg
    calculator.stored_operations.append(input)

def run(calculator):
    text = ''
    # Run until user types quit
    while text != 'quit':
        # Take input from user
        text = input('Enter calculation: ')
        # Split input into a list. Only splits if value contains anything which handles dubble space. Also makes all string lowercase.
        text = [substring.lower() for substring in text.split(' ') if substring]
        # Check type of input, here text[0] is the register, text[1] is the operation, and text[2] is the value to do the operation with.
        if len(text) == 3:
            # Operation
            for reg in calculator.register_list:
                #Check if register already exists
                if reg.name == text[0]:
                    calculator.make_calculation(reg, text)
                    break
            else:
                # Did not have register, create new one and add to register_list if we got a correct operation
                if text[1] in calculator.operation_list:
                    if text[2].isdigit():
                        reg = Register(text[0], int(text[2]))
                        calculator.register_list.append(reg)
                    else:
                        # Tries to make operations between registers, if they do not exist add them and also store operation.
                        reg1 = Register(text[0], 0)
                        calculator.register_list.append(reg1)
                        store_lazy_evaluations(calculator, text, reg1)
                else:
                    print('Invalid operation, must be: add, subtract, or multiply')
                    
        # Check if input was to print                    
        elif len(text) == 2:
            if text[0] == 'print':
                # Calculate lazy evaluations, here stored is in form [register, operation, register], 
                # last is a list that holds the calculations of the register we want to print
                last = []
                for stored in calculator.stored_operations:
                    # Skip since these caluculation should be done last
                    if stored[0].name == text[1]:
                        last.append([stored[0], stored])
                        continue
                    # Change last place in stored from register to the value of that register in order for make_calculations()
                    # to be able to handle it
                    stored[2] = stored[2].value
                    stored[2] = str(stored[2])
                    calculator.make_calculation(reg, stored)
                calculator.stored_operations = []
                # Make last calculations
                for operation in last:
                    operation[1][2] = operation[1][2].value
                    operation[1][2] = str(operation[1][2])
                    calculator.make_calculation(operation[0], operation[1])
                # Print register
                for reg in calculator.register_list:
                    if reg.name == text[1]:
                        print(reg.value)
                        break
                else:
                    print('The given register does not exist.')
            else:
                print('Invalid input.')
        else:
            # Quit or invalid input
            if text[0] == 'quit':
                break
            else:
                print('Invalid input.')

"""
Initialize program with all lists that the class Calculator takes and also the operations we allow.
"""
register_list = []
operation_list = ['add', 'subtract', 'multiply']
stored_operations = []
calc = Calculator(register_list, operation_list, stored_operations)
run(calc)