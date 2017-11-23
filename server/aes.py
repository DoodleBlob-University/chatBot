import base64
import hashlib
from Crypto import Random ### imported Random from Crypto <https://pypi.python.org/pypi/pycrypto> - 09/11/17
from Crypto.Cipher import AES ### imported AES from Crypto.Cipher <https://pypi.python.org/pypi/pycrypto> - 09/11/17

class AESEncryption(object):
### Charlie Barry
    def __init__(self, key):
        self.bs = 32    #AES block size
        self.key = hashlib.sha256(key.encode()).digest()    #Applies SHA265 Hash to the encoded key, then digests using hashlib

### Code from Stack Overflow Post about AES Encryption <https://stackoverflow.com/questions/12524994/encrypt-decrypt-using-pycrypto-aes-256> 9/11/2017
    def encrypt(self, plaintext):
        plaintext = self._pad(plaintext)    #Pads plaintext so its size is a multiple of 16 bytes
        init = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CFB, init) ### Charlie Barry
        return base64.b64encode(init + cipher.encrypt(plaintext))

    def decrypt(self, encryptedStr):
        encryptedStr = base64.b64decode(encryptedStr)
        init = encryptedStr[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CFB, init) ### Charlie Barry
        return self._unpad(cipher.decrypt(encryptedStr[AES.block_size:])).decode('utf-8')

    def _pad(self, s):
        return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)

    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s)-1:])]
