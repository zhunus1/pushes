import os
from django.utils import timezone
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding

BLOCK_SIZE = 256
VECTOR_SIZE = 16

def get_hash(plain):
    digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
    digest.update(plain.encode())
    return digest.finalize()

def encrypt(string_hex, key):
    # Gets string hex, returns hex cipher
    iv = os.urandom(VECTOR_SIZE)
    padder = padding.PKCS7(BLOCK_SIZE).padder()
    payload = padder.update(string_hex.encode()) + padder.finalize()
    h = get_hash(key)
    cipher = Cipher(algorithms.AES(h), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = iv + encryptor.update(payload) + encryptor.finalize()
    return ciphertext.hex()

def decrypt(string_hex, key):
    # Gets cipher hex, returns hex string
    b = bytes.fromhex(string_hex)
    iv, b = b[:VECTOR_SIZE], b[VECTOR_SIZE:]
    unpadder = padding.PKCS7(BLOCK_SIZE).unpadder()
    h = get_hash(key)
    cipher = Cipher(algorithms.AES(h), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    payload = decryptor.update(b) + decryptor.finalize()
    return (unpadder.update(payload) + unpadder.finalize()).decode()
