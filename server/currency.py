#CurrencyAPI
import requests ### imported module requests <https://pypi.python.org/pypi/requests> 9/11/2017

class currency(object):
    def __init__(self):
        self.key = '37d9bd361185111f6420d35bdec31f45'

    def convert(self, cFrom, cTo, amount):
        """Takes two strings and a float as an input and outputs a floating point number as a string"""
        cFrom = "USD" + cFrom.upper()
        cTo = "USD" + cTo.upper()
        amount = float(amount)
        curr = requests.get('http://apilayer.net/api/live?access_key={}'.format(self.key)) #requests JSON file and formats key from __init__
        curr = curr.json() #reads JSON file and stores as curr
        if curr['success']: #checks success is found within JSON
            quotes = curr['quotes'] #selects the quotes key
            cFromNum=amount/quotes[cFrom] #converts cFrom to USD
            cToNum = cFromNum*quotes[cTo] #converts cFromNum to requested currency
            return str(round(cToNum,2))
        else:
            return ""

    def inputStr(self, userinput):
        """Takes userInput as a string and outputs dictionary"""
        userinput = userinput.split(' ')
        response = {}
        for word in userinput:
            if word == "to":
                try:
                    amount = userinput[userinput.index(word)-2] #gets word that is two words before where "to" is found and stores as amount
                    response['amount'] = str(round(float(amount),2))  #rounds amount to 2dp and converts to string
                    response['cFrom'] = userinput[userinput.index(word)-1] #gets word before "to" is found and stores as cFrom
                    response['cTo'] = userinput[userinput.index(word)+1] #gets word after "to" is found and stores as cTo
                except:
                    response = {}
        return response
