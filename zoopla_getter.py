from zoopla import Zoopla

zoopla = Zoopla(api_key='hmzgmvxhz4p9feptarrjchy7')





#print(zoopla.area_value_graphs({'postcode': 'w12', 'output_type': 'outcode',
#                                'size'    : 'large'}))


def find_houses(monthly, deposit, annual_income, postcode,
                radius, n_beds, multiplier=4.5):
    search = zoopla.property_listings({
        'postcode'      : postcode,
        'radius'        : radius,
        'minimum_beds'  : n_beds,
        'maximum_beds'  : n_beds,
        'page_size'     : 100,
        'maximum_price' : annual_income * multiplier,
        'listing_status': 'sale'})
    for result in search.listing:
        print(result.price)
        print(result.displayable_address)
        print(result.image_url)
    return search


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

find_houses(10,200, 50000, 'w12', 10, 2)