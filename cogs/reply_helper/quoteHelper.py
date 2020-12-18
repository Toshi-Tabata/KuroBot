import random

"""
Module for abstracting quote functions
"""

def get_quote(args):
    with open("KuroQuotes.txt") as file:
        quotes = list(file)
        quoteToSend = []
        for arg in args:
            try:
                index = int(arg)
                quote = quotes[index].split("\\n")

            except (ValueError, IndexError):
                quote = random.choice(quotes)
                quote = quote.split("\\n")
            
            for q in quote:
                quoteToSend.append(q)

        # Send the list of quotes if we managed to get any
        if quoteToSend:
            return quoteToSend
        else:
            # We didn't get any valid args
            quote = random.choice(quotes)
            parsed_quote = quote.split("\\n")
            return parsed_quote
