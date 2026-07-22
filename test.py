from app.utils.encryption import encrypt,decrypt
from app.utils.lookup import encrypt_hash

original_email = "vansh12@gmail.com"

document_ = encrypt(original_email)

document_in= encrypt_hash(original_email)

print(document_)
print(document_in)