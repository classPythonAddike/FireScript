class Expression():
    def __init__(self, value: 'Expression'):
        self.value = value

    def eval(self) -> str:
        return self.value.eval()

    @property
    def type(self) -> str:
        return self.__class__.__name__

    def __repr__(self) -> str:
        return f"<Expression: {self.type}>"


"""
FireScript is Queue based - First In First Out
"""

class PrintExp(Expression):
    def eval(self) -> str:
        return f"{self.value.eval()}PRINT\nPOP\n"

class AddExp(Expression):
    def __init__(self, lval: Expression, rval: Expression):
        self.lval = lval
        self.rval = rval

    def eval(self) -> str:
        return f"{self.lval.eval()}{self.rval.eval()}ADD\nPOP\nPOP\n"

class IntExp(Expression):
    def __init__(self, value: int):
        self.value = value

    def eval(self) -> str:
        return f"PUSH {self.value}\n"
