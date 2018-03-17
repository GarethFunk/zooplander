from zoopla import Zoopla

zoopla = Zoopla(api_key='hmzgmvxhz4p9feptarrjchy7')

#search = zoopla.property_listings({
#    'maximum_beds': 2,
#    'page_size': 100,
#    'listing_status': 'sale',
#    'area': 'Blackley, Greater Manchester'
#})
#
#for result in search.listing:
#    print(result.price)
#    print(result.description)
#    print(result.image_url)


print(zoopla.area_value_graphs({'postcode':'w12', 'output_type': 'outcode',
                          'size': 'large'}))