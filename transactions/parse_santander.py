import requests
import lib.obp
from settings import *
import pandas as pd

obp = lib.obp

obp.setBaseUrl(BASE_URL)
obp.setApiVersion(API_VERSION)

# Login and set authorized token
obp.login(USERNAME, PASSWORD, CONSUMER_KEY)

our_bank = OUR_BANK

accounts = obp.getPrivateAccounts(our_bank)
our_account = accounts[0]['id']

transactions = obp.getTransactions(our_bank, our_account)

print("Got {0} transactions".format(len(transactions)))

#pd.read_json(path_or_buf = transactions)

