import requests
import json
from .location import Location

class MondayItem:

    def __init__(self, apiKey, itemID, itemName="", pulseID=False):
        self.apiUrl = "https://api.monday.com/v2"
        self.headers = {"Authorization": apiKey, "API-Version": "2023-04"}

        if pulseID:
            pulse_item_data = self.get_item(itemID)
            print(pulse_item_data)
            self.ID = pulse_item_data.get("Project ID")
        else:
            self.ID = itemID

        self.name = itemName
        self.data = self.get_item(self.ID)

    

    def get_item(self, itemID):
        # GraphQL query to fetch the item details by itemID
        query = f"""query {{
        items (ids: {itemID}) {{
            column_values {{
            column {{
                id
                title
            }}
            id
            type
            value
            }}
        }}
        }}"""

        # Send the POST request to the Monday.com API
        data = {'query': query}
        response = requests.post(url=self.apiUrl, json=data, headers=self.headers)

        # Check if the request was successful
        if response.status_code == 200:
            # Load the response data
            data = response.json()
            item = data.get('data', {}).get('items', [])[0]  # Access the first (and only) item
            column_values = item.get('column_values', [])
            
            result = {column_value.get('column', {}).get('title'): column_value.get('value') 
                    for column_value in column_values if column_value.get('column', {}).get('title')}
            return result
        else:
            return {"error": f"Failed to fetch item, status code: {response.status_code}"}  # change later

    def get_data(self):
        return self.data

    def get_snuggpro_job_creation_data(self):
        def us_phone_formatter(phone):
            phone = str(phone)
            return '(' + phone[-10:-7] + ') ' + phone[-7:-4] + '-' + phone[-4:]

        def us_address_formatter(full_address):
            parts = full_address.split(",")
            parts.pop()
            state = parts.pop().strip()
            city = parts.pop().strip()
            street_address = ''.join(parts)
            return street_address, city, state

        first_name = self.name.split()[0]
        last_name = self.name.split()[-1]
        email = json.loads(self.data.get("Email Address")).get("email")
        phone = us_phone_formatter(json.loads(self.data.get("Phone Number")).get("phone"))
        
        full_address = json.loads(self.data.get("Location")).get("address")
        coordinate = (json.loads(self.data.get("Location")).get("lat"), json.loads(self.data.get("Location")).get("lng"))
        address1, city, state = us_address_formatter(full_address) 
        
        location = Location(coordinate[0], coordinate[1])
        zip_code = location.get_zipcode()

        return {
            "firstName": first_name,
            "lastName": last_name,
            "email": email,
            "homePhone": phone,
            "address1": address1,
            "city": city,
            "state": state,
            "zip": zip_code,
        }