import rncryptor

data = '4'
password = 'secret'

# rncryptor.RNCryptor's methods
cryptor = rncryptor.RNCryptor()
encrypted_data = cryptor.encrypt(data, password)
print(encrypted_data.hex())
decrypted_data = cryptor.decrypt(encrypted_data, password)
print(decrypted_data)
assert data == decrypted_data

# rncryptor's functions
encrypted_data = rncryptor.encrypt(data, password)
print(encrypted_data)
decrypted_data = rncryptor.decrypt(encrypted_data, password)
assert data == decrypted_data