import pandas as pd
from datetime import date, timedelta
from schedule import available_appointments, get_time_slots

import sys
print(sys.path)

# Assuming you have a dataframe named 'df' with booked appointments data
# Initialize list of lists
data = [[date(2023, 6, 1), '8:00 Am', 'DXLF'], [date(2023, 6, 1), '8:04 Am', 'DXLF'], [date(2023, 6, 1), '11:50 Am', 'PNS'], 
    [date(2023, 6, 1), '10:00 Am', 'DXLF'],
    [date(2023, 6, 2), '8:00 Am', 'DXLF'],[date(2023, 6, 1), '8:50 Am', 'DXLF'],[date(2023, 6, 1), '8:20 Am', 'DXLF'],
    [date(2023, 6, 3), '8:00 Am', 'DXLF'],[date(2023, 6, 3), '8:10 Am', 'DXLF'],[date(2023, 6, 3), '8:20 Am', 'DXLF'],
    [date(2023, 6, 3), '10:00 Am', 'DXLF'],[date(2023, 6, 3), '10:10 Am', 'DXLF'],[date(2023, 6, 3), '11:50 Am', 'PNS'],
    [date(2023, 6, 1), '8:20 Am', 'DXLF'],[date(2023, 6, 1), '8:30 Am', 'DXLF'],[date(2023, 6, 1), '8:40 Am', 'DXLF']]

# Create the pandas DataFrame
df = pd.DataFrame(data, columns = ['Date', 'Time','Procedure'])

# Call the available_appointments function to get the available appointments for the next 7 days
num_days = 7
available_slots_df = available_appointments(df, 'DXLF', num_days)

# Print the available slots dataframe
print("Available Appointments:")
print(available_slots_df)

# Call the get_time_slots function to extract the time slots from the available slots dataframe
time_slots = get_time_slots(available_slots_df)

# Print the extracted time slots
print("Available Time Slots:")
for slot in time_slots:
    print(slot)
print(type(time_slots[0]))
