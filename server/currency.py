#CurrencyAPI
import requests

class currency(object):
    def __init__(self):
        self.key = '37d9bd361185111f6420d35bdec31f45'

    def convert(self, cFrom, cTo, amount):
        cFrom = "USD" + cFrom.upper()
        cTo = "USD" + cTo.upper()
        amount = float(amount)
        curr = requests.get('http://apilayer.net/api/live?access_key={}'.format(self.key))
        curr = curr.json()
        if curr['success']:
            quotes = curr['quotes']
            cFromNum=amount/quotes[cFrom]
            cToNum = cFromNum*quotes[cTo]
            return str(round(cToNum,2))
        else:
            return ""

    def inputStr(self, userinput):
        userinput = userinput.split(' ')
        response = {}
        for word in userinput:
            if word == "to":
                try:
                    amount = userinput[userinput.index(word)-2]
                    response['amount'] = str(round(float(amount),2))
                    response['cFrom'] = userinput[userinput.index(word)-1]
                    response['cTo'] = userinput[userinput.index(word)+1]
                except:
                    response = {}
        return response
