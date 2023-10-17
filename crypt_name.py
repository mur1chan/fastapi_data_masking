from cryptography.fernet import Fernet


class Pseudonymize:
    def setup(self):
        self.key = self.read_key()
        print(f"Read key: {self.key}")
        self.cipher_suite = Fernet(self.key.encode())  # Convert the key string to bytes

    def read_key(self):
        with open("key.txt", "r") as f:
            key = f.read().strip()  # Remove any extra spaces or newlines
        return key

    def generate_key(self):
        key = Fernet.generate_key()
        print(f"Fernet Key: {key.decode()}")  # Decode bytes to string for printing
        choice = input("Do you want to store the key into a textfile? [y/n]: ")
        if choice == "y":
            with open("key.txt", "w") as f:
                f.write(key.decode())  # Decode bytes to string for storing
        elif choice == "n":
            pass
        else:
            print("Wrong input. Try again.")

    def pseudonymize(self, data):
        return self.cipher_suite.encrypt(data.encode()).decode()

    def depseudonymize(self, data):
        return self.cipher_suite.decrypt(data.encode()).decode()

