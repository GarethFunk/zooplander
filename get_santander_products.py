import obp
from settings import *


obp.setBaseUrl(BASE_URL)
obp.setApiVersion(API_VERSION)

# Login and set authorized token
obp.login(USERNAME, PASSWORD, CONSUMER_KEY)

def get_bank_products(OUR_BANK):
    products = obp.get_bank_services(OUR_BANK)
    return products

if __name__ == '__main__':
    print(get_bank_products(OUR_BANK))