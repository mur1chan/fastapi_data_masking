import gocept.pseudonymize


class Pseudonymize:
    def __init__(self):
        self.pseudo = gocept.pseudonymize

    def pseudo_name(self, name:str, salt:str):
        pseudo_name = self.pseudo.name(name, salt)
        return pseudo_name

    def pseudo_street(self, street:str, salt:str):
        pseudo_street = self.pseudo.street(street, salt)
        return pseudo_street

    def pseudo_postal(self, postal_code:int, salt:str):
        pseudo_postal = self.pseudo.integer(postal_code, salt)
        return pseudo_postal

    def pseudo_city(self, city:str, salt:str):
        pseudo_city = self.pseudo.text(city, salt)
        return pseudo_city

