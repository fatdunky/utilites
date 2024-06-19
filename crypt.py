'''
Created on 23Nov.,2016

@author: fatdunky
'''
import base64
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto import Random


def encrypt(key, source, encode=True):
    # source = base64.b64encode(source).decode("latin-1")
    # key = base64.b64encode(key).decode("latin-1")
    key = SHA256.new(str.encode(key)).digest()  # use SHA-256 over our key to get a proper-sized AES key
    IV = Random.new().read(AES.block_size)  # generate IV
    encryptor = AES.new(key, AES.MODE_CBC, IV)
    padding = AES.block_size - len(source) % AES.block_size  # calculate needed padding
    # source += bytes([padding]) * padding  # Python 2.x: source += chr(padding) * padding
    source += chr(padding) * padding
    data = IV + encryptor.encrypt(str.encode(source))  # store the IV at the beginning and encrypt
    return base64.b64encode(data).decode("latin-1") if encode else data

def decrypt(key, source, decode=True):
    if not source: 
        return ""
    if decode:
        source = base64.b64decode(source.encode("latin-1"))
    key = SHA256.new(str.encode(key)).digest()  # use SHA-256 over our key to get a proper-sized AES key
    IV = source[:AES.block_size]  # extract the IV from the beginning
    decryptor = AES.new(key, AES.MODE_CBC, IV)
    data = decryptor.decrypt(source[AES.block_size:])  # decrypt
    padding = data[-1]  # pick the padding value from the end; Python 2.x: ord(data[-1])
    # padding = ord(data[-1])
    if data[-padding:] != bytes([padding]) * padding:  # Python 2.x: chr(padding) * padding
    # if data[-padding:] != chr(padding) * padding:  # Python 2.x: chr(padding) * padding
        raise ValueError("Invalid padding...")
    return data[:-padding]  # remove the padding
