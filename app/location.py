from geopy.geocoders import Nominatim

class Location:
    def __init__(self, latitude, longitude):
        self.latitude = latitude
        self.longitude = longitude
        self.geolocator = Nominatim(user_agent="geoapiExercises")

    def get_zipcode(self):
        try:
            location = self.geolocator.reverse((self.latitude, self.longitude), exactly_one=True)
            if location and 'postcode' in location.raw['address']:
                return location.raw['address']['postcode']
            else:
                return "ZIP code not found"
        except Exception as e:
            return f"Error occurred: {e}"