import base64
import hashlib
from Crypto import Random
from Crypto.Cipher import AES

class AESEncryption(object):

    def __init__(self, key):
        self.bs = 32
        self.key = hashlib.sha256(key.encode()).digest()

    def encrypt(self, plaintext):
        plaintext = self._pad(plaintext)    #Pads plaintext so its size is a multiple of 16 bytes
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CFB, iv)
        return base64.b64encode(iv + cipher.encrypt(plaintext))

    def decrypt(self, encryptedStr):
        encryptedStr = base64.b64decode(encryptedStr)
        iv = encryptedStr[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CFB, iv)
        return self._unpad(cipher.decrypt(encryptedStr[AES.block_size:])).decode('utf-8')

    def _pad(self, s):
        return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)

    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s)-1:])]
