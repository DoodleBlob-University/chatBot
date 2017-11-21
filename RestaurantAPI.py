##### Function to search google places ratings!!!!!!! #####
def getGooglePlacesRatings(restaurants):
    # 'restaurants': array of dictionaries = [{u"name":u"Jimbo's",u"location":u"Coventry"},{u"name":u"Taste of China",u"location":u"London"}]
 
    # Set google places api
    from googleplaces import GooglePlaces, types, lang
    google_places_api_key = 'AIzaSyDQ-mcgK1gSnI6soXWZnAA2Z9MeDnb5ZRo'
    google_places = GooglePlaces(google_places_api_key)
     
    #Search restaurants
    for restaurant in restaurants:
        restaurantFound = 0
        restaurantName = restaurant["name"].lower()
        restaurantLocation = restaurant["location"].lower()
 
        query_result = google_places.nearby_search(keyword=restaurantName, location=restaurantLocation, radius="50000", types=[types.TYPE_FOOD], sensor="false")
         
        # Loop query results
        for place in query_result.places:
            if (restaurantName == place.name.lower() or
                'restaurant ' + restaurantName  == place.name.lower() or
                'restaurante ' + restaurantName == place.name.lower() or
                restaurantName + ' restaurant'  == place.name.lower() or
                restaurantName + ' restaurante'  == place.name.lower() or
                'restaurant ' + place.name.lower()  == restaurantName or
                'restaurante ' + place.name.lower() == restaurantName or
                place.name.lower() + ' restaurant'  == restaurantName or
                place.name.lower() + ' restaurante'  == restaurantName
                ):
                place.get_details() """This iteration checks the possible combinations of """
                if 'user_ratings_total' in place.details:
                    restarurantNumRatings=place.details['user_ratings_total']
                else:
                    restarurantNumRatings='-'
                result = (place.name, '\t', place.rating, '\t', restarurantNumRatings) """\t will cause the printed output to tab, making for neater presenation"""
                restaurantFound = 1
                break

    return(result)
