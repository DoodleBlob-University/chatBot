import unittest

class testServer(unittest.TestCase):
    
    def setUp(self):
        from server import server
        self.server = server('', 1143, 'gbaei395y27ny9')

    def test_getIpData(self):
        self.assertEqual(self.server.getIpData('8.8.8.8')['status'], 'success')
        self.assertEqual(self.server.getIpData('')['status'], 'success')
        self.assertEqual(self.server.getIpData('127.0.0.1')['status'], 'success')

    def test_searchJSON(self):
        self.assertEqual(self.server.searchJSON('Hi what is the weather today ?'), ['weather', 'time'])
        self.assertEqual(self.server.searchJSON('Is it going to rain today ?'), ['weather', 'time'])

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
