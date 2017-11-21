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
        self.assertEqual(self.server.searchJSON(''), [])
        self.assertEqual(self.server.searchJSON('Where can i see a film'), ['cinema'])
        self.assertEqual(self.server.searchJSON('Hi what is the weather today ?'), ['weather'])
        self.assertEqual(self.server.searchJSON('Is it going to rain today ?'), ['weather'])

class weather(unittest.TestCase):
    def setUp(self):
        from weather import weather
        self.weather = weather
    
    def test_unixTimeToDateTime(self):
        self.assertEqual(self.weather.unixTimeToDateTime('1511276400'), '2017-11-22 15:00')

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

class currency(unittest.TestCase):
    def setUp(self):
        from currency import currency
        self.currency = currency
    
    def test_notReturnBlank(self):
        self.assertNotEqual(self.currency, "")

if __name__ == '__main__':
    unittest.main()
