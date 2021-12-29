class Token():
    def __init__(self, value: str):
        self.value = value
    
    @property
    def type(self) -> str:
        return self.__class__.__name__

    def __repr__(self) -> str:
        return f"<Token {self.type}: {self.value}>"


class Identifier(Token):
    pass


class Integer(Token):
    def __init__(self, value: str):
        self.value = int(value)

class Float(Token):
    def __init__(self, value: str):
        self.value = float(value)

class String(Token):
    pass


class NewLine(Token):
    def __repr__(self) -> str:
        return f"<Token {self.type}: \\n>"


class Operator(Token):
    pass

class EqualTo(Token):
    pass


class Bracket(Token): # ()
    pass

class SquareBracket(Token): # []
    pass

class CurlyBracket(Token): # {}
    pass

class AngleBracket(Token): # <>
    pass

class EOF(Token):
    pass
