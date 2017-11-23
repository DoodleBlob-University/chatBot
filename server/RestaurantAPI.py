##### Function to search google places ratings!!!!!!! #####
def getGooglePlaces(restaurants, location, keyword):
    # 'restaurants': array of dictionaries = [{u"name":u"Jimbo's",u"location":u"Coventry"}
    """Set google places api"""
    from googleplaces import GooglePlaces, types, lang
    google_places_api_key = 'AIzaSyDQ-mcgK1gSnI6soXWZnAA2Z9MeDnb5ZRo'
    google_places = GooglePlaces(google_places_api_key)
      
    query_result = google_places.nearby_search(location, keyword,radius=1000, types=[types.TYPE_RESTAURANT])

    try:
    if query_result.has_attributions:
        queryResult = (query_result.html_attributions)

    for place in query_result.places:
        name = (place.name)
        geoLocation = (place.geo_location)
        placeId = (place.place_id)
         
        """Check and grab restaurant details"""
        for place in query_result.places:
            if (restaurantName == place.name.lower() or
                'restaurant ' + restaurantName  == place.name.lower() or
                restaurantName + ' restaurant'  == place.name.lower() or
                'restaurant ' + place.name.lower()  == restaurantName or
                place.name.lower() + ' restaurant'  == restaurantName):
                place.get_details() 
                if 'user_ratings_total' in place.details:
                    restarurantNumRatings=place.details['user_ratings_total']
                else:
                    restarurantNumRatings='-'
                result = (place.name, '\t', place.rating, '\t', restarurantNumRatings) #\t will tab the results 
                restaurantFound = 1
                break
                
    except:
        result = ("Not a valid restaurant")
                    
    return(result, queryResult, name, geoLocation, placeId)
