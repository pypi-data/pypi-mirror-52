from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
from Crypto.Protocol.KDF import PBKDF2
from base64 import b64decode, b64encode
import os

def generate_RSA():
    privateKey = RSA.generate(2048)
    return privateKey.publickey().export_key(), privateKey.export_key()

def encryptKey(key, password):
    derivedKey = PBKDF2(password, password, 16)
    cipher = AES.new(derivedKey, AES.MODE_GCM)
    iv = cipher.nonce
    encrypted, tag = cipher.encrypt_and_digest(key)
    return b64encode(encrypted), b64encode(iv)

def decryptKey(encryptedkey, iv, password):
    derivedKey = PBKDF2(password, password, 16)
    iv = b64decode(iv)
    cipher = AES.new(derivedKey, AES.MODE_GCM, nonce=iv)
    decrypted = cipher.decrypt(b64decode(encryptedkey))
    return decrypted

def generateKeys(password):
    sPublicKey, sPrivateKey = generate_RSA()
    ePublicKey, ePrivateKey = generate_RSA()
    sPrivateKey, ivs = encryptKey(sPrivateKey, password)
    ePrivateKey, ive = encryptKey(ePrivateKey, password)
    return {
        "IV": {
            "IVE": ive.decode(),
            "IVS": ivs.decode()
            },
        "ePublicKey": ePublicKey.decode(),
        "ePrivateKey": ePrivateKey.decode(),
        "sPublicKey": sPublicKey.decode(),
        "sPrivateKey": sPrivateKey.decode()
        }
    
def generate_aes_key() -> "bytes" :
    """generate random AES key (-> aes_secret)"""
    secret = os.urandom(32)
    return secret

def create_access_key(aes_key, public_key):
    """encrypt AES key to get access key (aes_secret, public_key -> access_key)"""
    rsaKey = RSA.import_key(public_key)
    cipher = PKCS1_OAEP.new(rsaKey)
    encrypted = cipher.encrypt(aes_key)
    return b64encode(encrypted)

def decrypt_access_key(access_key, private_key):
    """Decrypt access key using RSA private Key(RSA_Key)"""
    access_key = b64decode(access_key)
    rsaKey = RSA.import_key(private_key)
    cipher = PKCS1_OAEP.new(rsaKey)
    decrypted = cipher.decrypt(access_key)
    return decrypted

def encrypt_file(bytes, aes_key):
    """encrypt file with key (f, aes_secret -> enc(f), iv)"""
    cipher = AES.new(aes_key, AES.MODE_GCM)
    iv = cipher.nonce
    encrypted, tag = cipher.encrypt_and_digest(bytes)
    return b64encode(encrypted), b64encode(iv)

def decrypt_file(file, aes_key, iv):
    file = b64decode(file)
    iv = b64decode(iv)
    cipher = AES.new(aes_key, AES.MODE_GCM, nonce=iv)
    decrypted = cipher.decrypt(file)
    return decrypted

def generate_signature(s, private_key):
    """generates signature base64encoded using RSA"""
    rsaKey = RSA.import_key(private_key)
    hash = SHA256.new(s.encode())
    cipher = pkcs1_15.new(rsaKey)
    signature = cipher.sign(hash)
    return b64encode(signature)

def get_publicKey(privateKey):
    rsaKey = RSA.import_key(privateKey)
    publicKey = rsaKey.publickey()
    return publicKey.export_key()