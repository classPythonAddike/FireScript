# Implement program readers - from file, stdin, etc

class Reader():
    def __init__(self):
        pass

    def advance_pointer(self):
        pass

    def retreat_pointer(self):
        pass

    def current_character(self) -> str:
        return ""

    def current_line(self) -> str:
        return ""


class FileReader(Reader):
    def __init__(self, file: str):
        self.pos = -1

        with open(file, "r") as f:
            self.code = f.read()
       
    def advance_pointer(self):
        self.pos += 1

    def retreat_pointer(self):
        if self.pos > 0: self.pos -= 1

    def current_character(self) -> str:
        if len(self.code) > self.pos >= 0:
            return self.code[self.pos]
        else:
            return "EOF"
    
    def current_line(self) -> str:
        pointer = 0

        for pos, line in enumerate(self.code.split("\n")):
            pointer += len(line + "\n")
            if pointer >= self.pos:
                return line

        return self.code.split("\n")[-1]
