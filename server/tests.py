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
        self.assertEqual(self.server.searchJSON('This has no keywords'), ([], {}))              #checks if response is correct when no keywords are present
        self.assertEqual(self.server.searchJSON('Hi what is the weather'), (['weather'], {}))   #tests whether it can recognise a keyword
        self.assertEqual(self.server.searchJSON('Is it going to rain in Coventry'), (['location', 'weather'], {'location': 'Coventry'}) or (['weather', 'location'], {'location': 'Coventry'})) #tests whether it can recognise a keyword and fetch location name

class weather(unittest.TestCase):
    def setUp(self):
        from weather import weather
        self.weather = weather

    def test_unixTimeToDateTime(self):
        self.assertEqual(self.weather.unixTimeToDateTime(self, '1511276400'), '2017-11-21 15:00')
        self.assertEqual(self.weather.unixTimeToDateTime(self, '910094199'), '1998-11-03 11:56')

class TestAES(unittest.TestCase):#Charlie and Dom
    '''tests aes to ensure that encrypted strings can be decrypted'''
    def setUp(self):
        from aes import AESEncryption
        self.aes = AESEncryption('this is a key')

    def test_encrypt(self):
        ciphertext = self.aes.encrypt("Hello World")
        self.assertEqual(64, len(ciphertext))

    def test_decrypt(self):
        ciphertext = b'URGaUFjpxuHHhQ21Cextqvi6/OegopSbcyQw9CxRRDMfeD5EnQIz6gt+JeH73+4g'
        self.assertEqual("Hello World", self.aes.decrypt(ciphertext))

    def test_encryptdecrypt(self):
        self.assertEqual("Hello World", self.aes.decrypt(self.aes.encrypt("Hello World")))

class currency(unittest.TestCase): #Thomas
    def setUp(self):
        from currency import currency
        self.currency = currency
<<<<<<< HEAD
    
    def test_currency(self):
        self.assertNotEqual(self.currency, "") #checks return is empty if unexpected input

        
=======

    def test_notReturnBlank(self):
        self.assertNotEqual(self.currency, "")
>>>>>>> bf41c91737620603836937f1266e44fef31232e6

class TestGeocode(unittest.TestCase):#Charlie
    '''tests both functions in geocode.py to see if they return the correct values'''
    def setUp(self):
        from geocode import geocode
        self.geocode = geocode()

    def test_getPlaceID(self):
        placeID = self.geocode.getPlaceID("Coventry")               #gets PlaceID of Coventry
        self.assertEqual("ChIJtyJuZVGxcEgRiQZPVvVg9gQ", placeID)    #checks if PlaceID is correct

    def test_getPlaceIDFAIL(self):
        placeID = self.geocode.getPlaceID("")   #inputs empty string
        self.assertEqual("", placeID)           #checks if status is NOT okay

    def test_getLocationCoords(self):
        location = self.geocode.getLocationCoords("Coventry")                       #gets coords of Coventry
        self.assertEqual({'latitude':52.406822,'longitude':-1.519693},location)     #checks if location is correct

if __name__ == '__main__':
    unittest.main()
