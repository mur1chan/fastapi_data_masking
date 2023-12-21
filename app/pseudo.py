import rncryptor

class Pseudonymize:
    def __init__(self):
        self.cryptor = rncryptor.RNCryptor()

    def pseudo(self, data:str, password:str):
        encrypted_data = self.cryptor.encrypt(data, password).hex()
        return encrypted_data

    def unpseudo(self, data:str, password:str):
        decrypted_data = self.cryptor.decrypt(bytes.fromhex(data), password)
        return decrypted_data