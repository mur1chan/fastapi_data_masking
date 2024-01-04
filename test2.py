import hashlib
hash_object = hashlib.sha256(b"Caroline")
hex_dig = hash_object.hexdigest()
print(hex_dig)