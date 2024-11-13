from app.mondayItem import MondayItem
from app.config import MONDAY_API_TOKEN

item_id = 7784749791
pulse_id = 7804194453
item_name = "Michael Anthony Carter"

# test_id_item =  MondayItem(MONDAY_API_TOKEN, item_id, item_name, pulseID=False)
# print(test_id_item.get_data())
# print(test_id_item.get_snuggpro_job_creation_data())
print("create object")
test_pulse_item = MondayItem(MONDAY_API_TOKEN, pulse_id, itemName=item_name, pulseID=True)
print("getting data")
print(test_pulse_item.get_data())
print("getting snuggpro creation data")
print(test_pulse_item.get_snuggpro_job_creation_data())

