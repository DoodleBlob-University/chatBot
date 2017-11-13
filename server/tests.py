#tests.py
import unittest

class TestAES(unittest.TestCase):

    def setUp(self):
        from aes import AESEncryption
        self.aes = AESEncryption('this is a key')

    def test_encrypt(self):
        ciphertext = self.aes.encrypt("Hello World")
        self.assertEqual(64, len(ciphertext))

    def test_decrypt(self):
        ciphertext = b'2IlEjjMDiSf96UTbgaYU8+SgYIWjKtGPJmpoCr/1pAJer0E5VeLhqH9arvgSPWEr'
        self.assertEqual("Hello World", self.aes.decrypt(ciphertext))

    def test_encryptdecrypt(self):
        self.assertEqual("Hello World", self.aes.decrypt(self.aes.encrypt("Hello World")))

if __name__ == '__main__':
    unittest.main()
