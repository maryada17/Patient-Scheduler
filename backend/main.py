from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from schedule import get_time_slots_schedule
from schedule import available_appointments 
from datetime import datetime, timedelta, date
import pandas as pd

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",  # Assuming React app is running on port 3000
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


# Initialize list of lists
data = [[date(2023, 6, 1), '8:00 Am', 'DXLF'], [date(2023, 6, 1), '8:04 Am', 'DXLF'], [date(2023, 6, 1), '11:50 Am', 'PNS'], 
    [date(2023, 6, 1), '10:00 Am', 'DXLF'],
    [date(2023, 6, 2), '8:00 Am', 'DXLF'],[date(2023, 6, 1), '8:50 Am', 'DXLF'],[date(2023, 6, 1), '8:20 Am', 'DXLF'],
    [date(2023, 6, 3), '8:00 Am', 'DXLF'],[date(2023, 6, 3), '8:10 Am', 'DXLF'],[date(2023, 6, 3), '8:20 Am', 'DXLF'],
    [date(2023, 6, 3), '10:00 Am', 'DXLF'],[date(2023, 6, 3), '10:10 Am', 'DXLF'],[date(2023, 6, 3), '11:50 Am', 'PNS'],
    [date(2023, 6, 1), '8:20 Am', 'DXLF'],[date(2023, 6, 1), '8:30 Am', 'DXLF'],[date(2023, 6, 1), '8:40 Am', 'DXLF']]

# Create the pandas DataFrame
df1 = pd.DataFrame(data, columns = ['Date', 'Time','Procedure'])

class TimeSlot(BaseModel):
    time_slot: str

class TimeSlotsResponse(BaseModel):
    timeSlots: list[str]

@app.get("/api/get-time-slots", response_model=TimeSlotsResponse)
async def get_time_slots():
    # Your code to fetch the time slots from the backend
    df = available_appointments(df1, 'DXLF', 5)
    time_slots = get_time_slots_schedule(df)
    time_slots = [str(slot) for slot in time_slots] 
    return TimeSlotsResponse(timeSlots=time_slots)


@app.post("/api/select-time-slot")
async def select_time_slot(time_slot: TimeSlot):
    # Handle the selected time slot in your backend logic
    print("Selected time slot:", time_slot.time_slot)
    # Perform further processing or store the selected time slot as needed
    return {"message": "Time slot selection received"}
