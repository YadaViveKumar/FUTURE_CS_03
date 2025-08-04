from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Hash import SHA256  

def derive_key(password, salt):
    return PBKDF2(password.encode(), salt, dkLen=32, count=100000, hmac_hash_module=SHA256)

def encrypt_file(file_data, password):
    salt = get_random_bytes(16)
    key = derive_key(password, salt)
    cipher = AES.new(key, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(file_data)
    return salt + cipher.nonce + tag + ciphertext

def decrypt_file(enc_data, password):
    salt = enc_data[:16]
    nonce = enc_data[16:32]
    tag = enc_data[32:48]
    ciphertext = enc_data[48:]
    key = derive_key(password, salt)
    cipher = AES.new(key, AES.MODE_EAX, nonce)
    return cipher.decrypt_and_verify(ciphertext, tag)
