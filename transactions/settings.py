

OUR_BANK     = 'santander.01.uk.sanuk'

USERNAME     = 'Emma.Uk.01'
PASSWORD     = 'X!fcfe91c5'
CONSUMER_KEY = 'lrswrw4jscchiaohpoebwks3mw15wpnujiz4e22x'

# API server URL https://apisandbox.openbankproject.com
#https://santander.openbankproject.com/my/logins/direct
#https://santander.openbankproject.com/
BASE_URL  = "https://santander.openbankproject.com/"
API_VERSION  = "v3.0.0"

# API server will redirect your browser to this URL, should be non-functional
# You will paste the redirect location here when running the script
CALLBACK_URI = 'http://127.0.0.1/cb'

# Our COUNTERPARTY account id (of the same currency)
OUR_COUNTERPARTY = '8ca8a7e4-6d02-48e3-a029-0b2bf89de9f0'
COUNTERPARTY_BANK = 'santander.01.uk.sanuk'
# this following two fields are just used in V210
OUR_COUNTERPARTY_ID = ''
OUR_COUNTERPARTY_IBAN = ''


# Our currency to use
OUR_CURRENCY = 'GBP'

# Our value to transfer
# values below 1000 do not require challenge request
OUR_VALUE = '0.01'
OUR_VALUE_LARGE = '1000.00'
