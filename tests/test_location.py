import pytest
from app.location import Location

@pytest.mark.parametrize("latitude, longitude, expected_zip", [
    (38.8977, -77.0365, "20500"),       # White House, Washington, D.C., USA
    (37.7749, -122.4194, "94103"),      # San Francisco, USA
    (48.8584, 2.2945, "75007"),         # Eiffel Tower, Paris, France
    (-19.0544, -169.8672, "ZIP code not found")  # Niue, no postcode
])

def test_get_zipcode_parametrized(latitude, longitude, expected_zip):
    location = Location(latitude, longitude)
    zip_code = location.get_zipcode()
    assert zip_code == expected_zip

def test_error():
    # Intentionally provide invalid coordinates to trigger an exception
    invalid_location = Location("invalid_latitude", "invalid_longitude")
    zip_code = invalid_location.get_zipcode()
    assert "Error occurred" in zip_code
