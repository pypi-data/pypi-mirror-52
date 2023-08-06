from .word_counter import run


class LevCore:
    def __init__(self):
        self.variables = {}

    def define(self, variable_name, value):
        self.variables[variable_name] = value

    def do(self, instruction_set):
        pass

    def but(self, instruction_set):
        pass

    def run(self):
        run(self.variables['vINPUT'])
