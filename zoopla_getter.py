from zoopla import Zoopla
import googlemaps
import urllib.request as rq
import re
import datetime
import numpy as np
import Financial_Data_Proc as fin
import lowest_level as lol


zoopla = Zoopla(api_key='hmzgmvxhz4p9feptarrjchy7')
gmaps = googlemaps.Client(key='AIzaSyD_PKC4yi-1Dh4qRcJkrda9Y8ZyFhyjKfw')


def get_historic_prices(outcode):
    content = rq.urlopen('http://api.zoopla.co.uk/api/v1/average_sold_prices.xml'
                         '?postcode={}&output_type=outcode&area_type=postcodes'
                         '&page_size=20&api_key=hmzgmvxhz4p9feptarrjchy7'.format(
        outcode)).read()
    splitten = str(content).split('<areas')
    houses = []
    averages = []
    for house in splitten:
        split_newline = house.split(r'\n')
        numbers = []
        for element in split_newline:
            if re.search(re.compile('year|http'), element):
                numbers.append(element)
        num2 = []
        for number in numbers:
            num2.append(re.findall('>.+<', number)[0])
        for i in range(len(num2)):
            num2[i] = num2[i].replace('>', '')
            num2[i] = num2[i].replace('<', '')
            if i < len(num2) - 1:
                num2[i] = float(num2[i])
        if len(num2) > 0:
            num2[-1] = num2[-1].split('/')[-1].replace('-', ' ')
            averages.append(_calc_historic_averages(num2))

    averages = np.array(averages)
    return averages[0, 0, :], np.nanmean(averages, axis=0)[1]


def _calc_historic_averages(last_years_list):
    now = datetime.datetime.now().year
    lasts = np.array([1,3,5,7])
    years = now - lasts
    last_years_list = np.array(last_years_list[:-1])
    prices = []
    for i in range(4):
        i += 1
        prod_sum = np.sum(last_years_list[:i] * last_years_list[4:i+4])
        num = np.sum(last_years_list[4:i+4])
        prices.append(prod_sum/num)
    return np.vstack((years, prices))


def pred_10y_prices(outcode, initial_savings, current_house_price):
    years, prices = get_historic_prices(outcode)
    annual_deposit = lol.read_globals()['annual_deposit']
    coeffs = np.polyfit(years, prices, 1)
    fore_years = np.arange(2018, 2029, 1)
    deposits = []
    for year in fore_years:
        deposits.append(fin.FutureDeposit(annual_deposit, year) +
                        initial_savings)
    preds = (coeffs[0]*fore_years + coeffs[1])*current_house_price/prices[0]
    return fore_years, deposits, preds

#print(_calc_historic_averages([0]))
#print(zoopla.area_value_graphs({'postcode': 'w12', 'output_type': 'outcode',
#                                'size'    : 'large'}))

#areas = zoopla.average_sold_prices({'postcode'  : 'W12', 'output_type':
#    'outcode', 'area_type' : 'postcodes'})
#print(areas)


def find_houses(annual_income, postcode, radius, n_beds, multiplier=4.5):

    search = zoopla.property_listings({
        'postcode'      : postcode,
        'radius'        : radius,
        'minimum_beds'  : n_beds,
        'page_size'     : 100,
        'maximum_price' : annual_income * multiplier,
        'listing_status': 'sale'})
    houses = []
    search_loc_geocode = gmaps.geocode(str(postcode) + " UK")
    search_loc = {"lat": search_loc_geocode[0]['geometry']['location']['lat'],
                  "lng": search_loc_geocode[0]['geometry']['location']['lng']}
    for result in search.listing:
        #print(result.price)
        #print(result.displayable_address)
        geocode_result = gmaps.geocode(str(result.displayable_address))
        if len(geocode_result) > 0:
            houses.append({'addr':str(result.displayable_address),
                           'price':float(result.price),
                           'lat':float(geocode_result[0]['geometry']['location']['lat']),
                           'lng':float(geocode_result[0]['geometry']['location']['lng'])})
        #print(result.image_url)
    return houses, search, search_loc


def get_mortgage(monthly_mortgage, deposit, house_price, term_in_years):
    # get available mortgages for a specific houser with a given price -
    # redirect to moneysupermarket.
    return


def get_stamp_duty(property_price, first_time_buyer=True):
    if first_time_buyer:
        if 0 < property_price < 300000:
            return 0.
        elif 300000 < property_price < 500000:
            return 0.05 * property_price
        else:
            pass
            # need additional stamp duty sophistication for more expensive
            # properties


#if __name__ == '__main__':
#    find_houses(50000, 'CB4', 10, 2)
