#CurrencyAPI
import requests

class currency(object):
    def __init__(self, recievedStr):
        self.input = recievedStr


    def convert(cFrom, cTo, amount):
        cFrom = "USD" + cFrom.upper()
        cTo = "USD" + cTo.upper()
        amount = float(amount)
        curr = requests.get('http://apilayer.net/api/live?access_key=37d9bd361185111f6420d35bdec31f45')
        curr = curr.json()
        quotes = curr['quotes']

        cFromNum=amount/quotes[cFrom]
        cToNum = cFromNum*quotes[cTo]
        return cToNum

    def inputStr(self, input):
        input = input.split(' ')
        response = ""

        for word in input:
            if word == "to":
                try:
                    response = input[input.index(word)-2]
                    response = str(round(float(response),2))
                    response += ":" + input[input.index(word)-1] + ":"
                    response += input[input.index(word)+1]
                except Exception as e:
                    response = ""
        return response
