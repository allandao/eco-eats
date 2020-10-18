

def searchDataSet(title, ingredients):
    # import json

    food_matched = "food"
    title_used = True # boolean for whether name or product was used (false meaning ingredients was used)
    land_use = 0.0
    animal_feed = 0.0
    farm = 0.2
    processing = 0.0
    transport = 0.1
    packaging = 0.0
    retail = 0.0
    total_emissions = 0.3
    eutrophying_emissions = 3.02
    total_emissions_with_eutrophying = land_use + animal_feed + farm + processing + transport + packaging + retail + eutrophying_emissions

    product_data = {
        'food_matched': food_matched,
        'title_used' : title_used,
        'land use': land_use,
        'animal feed': animal_feed,
        'farm': farm,
        'processing': processing,
        'transport': transport,
        'packaging': packaging,
        'retail': retail,
        'total emissions': total_emissions,
        'eutrophying emissions': eutrophying_emissions,
        'rating': 6,
        'total emissions with eutrophying': total_emissions_with_eutrophying
    }
    return product_data

# print(searchDataSet("apple", ""))