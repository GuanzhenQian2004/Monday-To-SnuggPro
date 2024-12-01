import pytest
from app.mondayItem import MondayItem
from app.config import MONDAY_API_TOKEN

@pytest.mark.parametrize("apiKey, itemID, itemName, pulseID", [
    (MONDAY_API_TOKEN, 6772214729, "Jeffrey Justice", False),       
])

def test_monday_item_initialization(apiKey, itemID, itemName, pulseID):
    newItem = MondayItem(apiKey, itemID, itemName, pulseID)
