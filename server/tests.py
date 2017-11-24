import unittest

class testServer(unittest.TestCase):

    def setUp(self):
        from server import server
        self.server = server('', 1143, 'gbaei395y27ny9')

    def test_getIpData(self): ### Dominc Egginton
        self.assertEqual(self.server.getIpData('8.8.8.8')['status'], 'success')
        self.assertEqual(self.server.getIpData('')['status'], 'success')
        self.assertEqual(self.server.getIpData('127.0.0.1')['status'], 'success')

    def test_formResponse(self): ### Dominic Egginton
        self.assertNotEqual(self.server.formResponse('Hey, what is the weather', '127.0.0.1', None), "Sorry, I don't understand what you are talking about.")
        self.assertNotEqual(self.server.formResponse('Whats the weather like in london?', '127.0.0.1', None), "Sorry, I don't understand what you are talking about.")
        self.assertNotEqual(self.server.formResponse('Can you get me the daily weather in Hinckley', '127.0.0.1', None), "Sorry, I don't understand what you are talking about.")
        self.assertNotEqual(self.server.formResponse('grab me the hourly weather', '127.0.0.1', None), "Sorry, I don't understand what you are talking about.")
        self.assertNotEqual(self.server.formResponse('1 gbp to usd', '127.0.0.1', None), "Sorry, I don't understand what you are talking about.")
        self.assertEqual(self.server.formResponse('open celery', '127.0.0.1', None), "/w/https://youtu.be/MHWBEK8w_YY")
        self.assertEqual(self.server.formResponse('get me the fucking weather', '127.0.0.1', None), "Please watch your language.")
        self.assertEqual(self.server.formResponse('Hey you whats up ?', '127.0.0.1', None), "Sorry, I don't understand what you are talking about.")
        self.assertEqual(self.server.formResponse('Whats my ip info ?', '8.8.8.8', None), "Your IP is 8.8.8.8, provided by Google.")

    def test_getServerIP(self):
        self.assertTrue(self.server.getServerIP()['external'] == self.server.getIpData('')['query'])

    def test_searchJSON(self): ### Charlie Barry
        self.assertEqual(self.server.searchJSON('This has no keywords'), ([], {}))              #checks if response is correct when no keywords are present
        self.assertEqual(self.server.searchJSON('Hi what is the weather'), (['weather'], {}))   #tests whether it can recognise a keyword
        keysFound, extraData = self.server.searchJSON('Is it going to rain in Coventry')
        self.assertEqual(extraData, {'location': 'Coventry'}) #tests whether it can recognise a keyword and fetch location name
        keysFound, extraData = self.server.searchJSON('10 gbp to usd')
        self.assertDictEqual(extraData, {'currency': {'amount': '10.0', 'cTo': 'usd', 'cFrom': 'gbp'}}) #tests whether returns a correct currency dictionary
        keysFound, extraData = self.server.searchJSON('woo this is a string woah here is the keyword daily and now it is gone')
        self.assertEqual(extraData, {'time' : 'daily'}) #tests whether it can fetch time from a string



    def closeSocket(self):
        self.server.socket.close()

class testWeather(unittest.TestCase): ### Dominic Egginton

    def setUp(self):
        from weather import weather
        self.weather = weather()

    def test_unixTimeToDateTime(self):
        self.assertEqual(self.weather.unixTimeToDateTime('1511276400'), '2017-11-21 15:00')
        self.assertEqual(self.weather.unixTimeToDateTime('910094199'), '1998-11-03 11:56')
        self.assertEqual(self.weather.unixTimeToDateTime('1511454788'), '2017-11-23 16:33')

    def test_weatherResponse(self):
        self.assertTrue('currently' in self.weather.forcastRequest({'latitude': '37.8267', 'longitude': '-122.4233'}))
        self.assertTrue('daily' in self.weather.forcastRequest({'latitude': '37.8267', 'longitude': '-122.4233'}))
        self.assertTrue('hourly' in self.weather.forcastRequest({'latitude': '37.8267', 'longitude': '-122.4233'}))

class TestAES(unittest.TestCase): ### Charlie Barry
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

class currency(unittest.TestCase): ### Thomas
    def setUp(self):
        from currency import currency
        self.currency = currency

    def test_currency(self):
        self.assertNotEqual(self.currency, "") #checks currency always returns something



class TestGeocode(unittest.TestCase): ### Charlie Barry
    '''tests both functions in geocode.py to see if they return the correct values'''
    def setUp(self):
        from geocode import geocode
        self.geocode = geocode()

    def test_getPlaceID(self):
        placeID = self.geocode.getPlaceID("Coventry")               #gets PlaceID of Coventry
        self.assertEqual("ChIJtyJuZVGxcEgRiQZPVvVg9gQ", placeID)    #checks if PlaceID is correct
        placeID = self.geocode.getPlaceID("")   #inputs empty string
        self.assertEqual("", placeID)           #checks if status is NOT okay

    def test_getLocationCoords(self):
        location = self.geocode.getLocationCoords("Coventry")                       #gets coords of Coventry
        self.assertEqual({'latitude':52.406822,'longitude':-1.519693},location)     #checks if location is correct

if __name__ == '__main__':
    unittest.main()
