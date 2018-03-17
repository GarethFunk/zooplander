from zoopla import Zoopla

zoopla = Zoopla(api_key='hmzgmvxhz4p9feptarrjchy7')





#print(zoopla.area_value_graphs({'postcode': 'w12', 'output_type': 'outcode',
#                                'size'    : 'large'}))

print(zoopla.average_sold_prices({'postcode'  : 'w12', 'output_type':
    'outcode', 'area_type' : 'postcodes'}))
def find_houses(annual_income, postcode, radius, n_beds, multiplier=4.5):
    search = zoopla.property_listings({
        'postcode'      : postcode,
        'radius'        : radius,
        'minimum_beds'  : n_beds,
        'maximum_beds'  : n_beds,
        'page_size'     : 100,
        'maximum_price' : annual_income * multiplier,
        'listing_status': 'sale'})
    houses = []
    for result in search.listing:
        #print(result.price)
        #print(result.displayable_address)
        houses.append((str(result.displayable_address), float(result.price)))
        #print(result.image_url)
    return houses, search


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
#    find_houses(50000, 'w12', 10, 2)
