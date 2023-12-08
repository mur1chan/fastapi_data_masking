import gocept.pseudonymize

class Pseudonymize:
    def __init__(self):
        self.pseudo = gocept.pseudonymize

    def pseudo_str(self, str:str, salt:str):
        string = self.pseudo.text(str, salt)
        return string

    def pseudo_int(self, int:int, salt:str):
        integer = self.pseudo.integer(int, salt)
        return integer