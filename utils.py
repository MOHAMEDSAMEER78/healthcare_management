import hashlib
import base64
from cryptography.fernet import Fernet

CIPHER_TEXT = "CipherTextSecretgAAAAABgJ9QJQ2Q7"

def protect_identity(name):
    # Hash the name to a UUID-like format
    hashed_name = hashlib.sha256(name.encode()).hexdigest()
    
    # Encrypt the hashed name
    key = Fernet.generate_key()
    cipher_suite = Fernet(key)
    cipher_text = cipher_suite.encrypt(hashed_name.encode())
    
    # Append "Anonymized" to the ciphertext
    anonymized_cipher_text = CIPHER_TEXT + base64.b64encode(cipher_text).decode()
    
    return anonymized_cipher_text, key

def decrypt_identity(anonymized_cipher_text, key):
    # Remove the "Anonymized" prefix
    cipher_text = base64.b64decode(anonymized_cipher_text.replace(CIPHER_TEXT, ""))
    
    # Decrypt the ciphertext
    cipher_suite = Fernet(key)
    plain_text = cipher_suite.decrypt(cipher_text)
    
    return plain_text.decode()

# Example usage:
name = "John Doe"
anonymized_cipher_text, key = protect_identity(name)
print("Protected identity:", anonymized_cipher_text)

decrypted_name = decrypt_identity(anonymized_cipher_text, key)
print("Decrypted identity:", decrypted_name)