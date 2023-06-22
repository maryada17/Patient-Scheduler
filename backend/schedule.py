
from datetime import datetime, timedelta, date
import numpy as np
import pandas as pd
import scipy.stats

def generate_procedure_time(mean, std_dev):
    '''
    Calculates time for the procedure based on mean and standard deviation.
    
    Args:
    mean: mean time for procedure
    std_dev: standard deviation for procedure

    Returns:
    time for the total procedure
    '''
    # Generate a random procedure time based on the provided mean and standard deviation
    procedure_time = np.random.normal(mean, std_dev)
    return timedelta(seconds=int(procedure_time))

def _get_appointment_duration(procedure:str, std:int = 2, mean:int = None):
    """
    Rotates an image (angle in degrees) and expands image to avoid cropping.

    Args:
    procedure: LRFA or DXLF or PNS
    std: number of standard deviations (default 2 standard deviations)
    mean: total mean time

    Returns:
    appointment_length: total appoinment time
    """
    process_mean = {'LRFA': 600, 'DXLF': 400, 'PNS': 600}
    process_std = {'LRFA': 180, 'DXLF': 100, 'PNS': 1200}
    if mean is None :
        mean = process_mean[procedure]
    else:
        mean = mean
    if std is None:
        std = process_std[procedure]
    else:
        std = std*process_std[procedure]
    return round((mean+std)/60.0)+1

def _time_difference(slot1, slot2):
    '''
    Calculate the time difference between two time slots.
    
    Args:
    slot1: Time which occurs first
    slot2: Time which occurs second

    Returns:
    duration: Finds the time difference in minutes.
    '''
    time_format = '%H:%M'
    time1 = datetime.strptime(slot1, time_format)
    time2 = datetime.strptime(slot2, time_format)
    duration = time2 - time1
    return duration.total_seconds() // 60  # Return the duration in minutes

def _add_minutes(time_str, minutes):
    '''
    Add  minutes from a given time..
    
    Args:
    time_str: Time 
    minutes: number of minutes to be added

    Returns:
    updated_time: updated time after addition
    '''
    time_format = '%H:%M'
    time_obj = datetime.strptime(time_str, time_format)
    updated_time = time_obj + timedelta(minutes=minutes)
    return updated_time.strftime(time_format)

def _sub_minutes(time_str, minutes):
    '''
    Subtract minutes from a given time..
    
    Args:
    time_str: Time 
    minutes: number of minutes to be subtracted

    Returns:
    updated_time: updated time after subtraction
    '''
    time_format = '%H:%M'
    time_obj = datetime.strptime(time_str, time_format)
    updated_time = time_obj - timedelta(minutes=minutes)
    return updated_time.strftime(time_format)

def _am_to_abs(time):
    '''
    Converts time with am/pm (01:00 pm) to 24 hour time format (13:00).
    
    Args:
    time: Time with am/pm 

    Returns:
    out_time: Time in 24 hour format.

    '''
    in_time = datetime.strptime(time,"%I:%M %p")
    out_time = datetime.strftime(in_time, "%H:%M")
    return out_time

    

def _find_available_time_slots(df, operation, physician_slots, slots, date):
    '''
    finds available time slots for a specified operation (procedure) and 
    physician slots (morning or evening) on a given date. The function 
    filters the DataFrame based on the date and physician slots. 
    calculates the quality score for each available time slot based on 
    the duration between appointments.
    
    Args: 
    df: dataframe with booked appointments.
    operation: 'DXLF' or 'PNS'
    physician_slots: Physician availability time slots. 
    slots: 'morning' or 'evening'.
    date: date for which we are searching appointment for the new patient.

    Returns:
    df_final: DataFrame containing the available slots, procedure, date, and quality score.
    '''
    # filtering dataframe based on date
    date_filter = (df['Date'] == date)
    df = df[date_filter] 
    #print("df after date", df)

    if slots == 'morning':
        phy_start_time = physician_slots[0][0]
        phy_end_time = physician_slots[0][1]
    else:
        phy_start_time = physician_slots[1][0]
        phy_end_time = physician_slots[1][1]

    # Initialize available time slots
    available_slots = []
    available_procedure = []
    available_date = []
    quality_scores = []
    df['abs'] = df.Time.apply(_am_to_abs) 

   
    # Convert DataFrame column to datetime objects
    if operation == 'DXLF':
        mean = 400
        std = 100
        if slots == "morning":
            filt = ( df['abs'] <=  phy_end_time)
            df = df[filt]
            # Sort DataFrame by time in ascending order
            df.sort_values(by='abs', inplace=True)
            #print(df,"df DXLF after sorting without indexing upto 12 pm")
            df = df.reset_index(drop=True)
            print(df,"df DXLF after changing index")
        else:
            filt = ( df['abs'] >=  phy_start_time)
            df = df[filt]
            # Sort DataFrame by time in ascending order
            df.sort_values(by='abs', inplace=True)
            df = df.reset_index(drop=True)
            print(df,"df dxlf after filtering from 1 pm to end")

        # Sort DataFrame by time in ascending order
        # df.sort_values(by='abs', inplace=True)
        # print(df,"df after sorting")

            # if df is completely empty
        if len(df) == 0:
            procedure_start_time = phy_start_time
            new_process_time = _get_appointment_duration(operation)
            procedure_end_time = _add_minutes(procedure_start_time, new_process_time)
            quality_score = 1
            available_slots.append((procedure_start_time, procedure_end_time))
            available_procedure.append(operation)
            available_date.append(date)
            quality_scores.append(quality_score)
            #print("procedure start time: ", procedure_start_time)
            #print("procedure end time: ", procedure_end_time)
            df_final = pd.DataFrame(list(zip(available_date, available_procedure, available_slots, quality_scores)),
               columns =['Date', 'Procedure', 'Available Slots', 'Quality Score'])
            #print(df_final, "df_final at len df 0")
            return df_final

        # Iterate through DataFrame to find available time slots
        for index, row in df.iterrows():
            current_time = row['abs']
            current_procedure = row['Procedure']
            process_time = _get_appointment_duration(current_procedure)
           
            current_time = _add_minutes(current_time, process_time)
            
            next_time = df.iloc[index + 1]['abs'] if index < len(df) - 1 else phy_end_time

            # Calculate time duration between current and next appointments
            duration = _time_difference(current_time, next_time)
            new_process_time = _get_appointment_duration(operation)
            if duration >= new_process_time:
                quality_score = 1
                
            elif duration > 0 and duration < new_process_time:
                #To find the probability using CDF cumulative Density Function
                quality_score = 1-scipy.stats.norm.cdf(mean,std,duration*60)
                
            else:
                continue

        # Find the available time slot for the new patient with the specified operation
            if current_time < phy_end_time:
                procedure_start_time = current_time
                procedure_end_time = min(_add_minutes(current_time, process_time), phy_end_time)
                
            else:
                procedure_start_time = None
                procedure_end_time = None

            # Add the available time slot to the list
            if procedure_start_time and procedure_end_time and procedure_start_time < procedure_end_time:
                available_slots.append((procedure_start_time, procedure_end_time))
                available_procedure.append(operation)
                available_date.append(date)
                quality_scores.append(quality_score)
                df_final = pd.DataFrame(list(zip(available_date, available_procedure, available_slots, quality_scores)),
               columns =['Date', 'Procedure', 'Available Slots', 'Quality Score'])
              
            
        return df_final
    
    if operation == 'PNS':
        mean = 600
        std = 1200

        if slots == "morning":
            filt = ( df['abs'] <=  phy_end_time)
            df = df[filt]

            # Sort DataFrame by time in ascending order
            df.sort_values(by='abs', ascending=False, inplace=True)
            df = df.reset_index(drop=True)
            print(df,"df after changing index")
        else:
            filt = ( df['abs'] >=  phy_start_time)
            df = df[filt]

            # Sort DataFrame by time in ascending order
            df.sort_values(by='abs', ascending=False, inplace=True)
            df = df.reset_index(drop=True)
            print(df,"df after filtering from 1 pm to end")
    
        # df completely empty
        if len(df) == 0:
            procedure_end_time = phy_end_time
            quality_score = 1
            new_process_time = _get_appointment_duration(operation)
            procedure_start_time = _sub_minutes(procedure_end_time, new_process_time)
            available_slots.append((procedure_start_time, procedure_end_time))
            available_procedure.append(operation)
            available_date.append(date)
            quality_scores.append(quality_score)
            df_final = pd.DataFrame(list(zip(available_date, available_procedure, available_slots, quality_scores)),
               columns =['Date', 'Procedure', 'Available Slots', 'Quality Score'])
    
            return df_final
            
       
        # Iterate through DataFrame to find available time slots
        for index, row in df.iterrows():
            current_time = row['abs']
            next_time = df.iloc[index + 1]['abs'] if index < len(df) - 1 else phy_start_time

            # only one data entry at physician entry time
            if current_time == next_time:
                procedure_end_time = phy_end_time
                process_time =  _get_appointment_duration(operation)
                procedure_start_time = _sub_minutes(procedure_end_time, process_time)
                available_slots.append((procedure_start_time, procedure_end_time))
                available_procedure.append(operation)
                available_date.append(date)
                quality_score = 1
                quality_scores.append(quality_score)
                df_final = pd.DataFrame(list(zip(available_date, available_procedure, available_slots, quality_scores)),
               columns =['Date', 'Procedure', 'Available Slots', 'Quality Score'])
                return df_final

            print(next_time,"next time")
            print(phy_start_time,"phy start time")
            if next_time != phy_start_time:
                next_procedure = df.iloc[index + 1]['Procedure']
                process_time = _get_appointment_duration(next_procedure)
                next_time= _add_minutes(next_time, process_time)
               
            # Calculate time duration between current and next appointments
            duration = -_time_difference(current_time, next_time)
            new_process_time = _get_appointment_duration(operation)
            if duration >= new_process_time:
                quality_score = 1
            elif duration > 0 and duration < new_process_time:
                #To find the probability using CDF cumulative Density Function
                quality_score = 1-scipy.stats.norm.cdf(mean,std,duration*60)
            else:
                continue

        # Find the available time slot for the new patient with the specified operation
            if next_time > phy_start_time:
                procedure_start_time = _sub_minutes(current_time, new_process_time)
                procedure_end_time = current_time
            else:
                procedure_start_time = None
                procedure_end_time = None

            # Add the available time slot to the list
            if procedure_start_time and procedure_end_time and procedure_start_time < procedure_end_time:
                available_slots.append((procedure_start_time, procedure_end_time))
                available_procedure.append(operation)
                available_date.append(date)
                quality_scores.append(quality_score)
                df_final = pd.DataFrame(list(zip(available_date, available_procedure, available_slots, quality_scores)),
               columns =['Date', 'Procedure', 'Available Slots', 'Quality Score'])
                return df_final

def available_appointments(df, operation, num_days):
        
        # Physician Availabality
        physician_slots = [("08:00","12:00"),("13:00","17:00")]
        
        # initialize today's date
        start_date = date(2023, 6, 1)
        df_list = []
        for single in range(num_days):
            available_time_slots = _find_available_time_slots(df, operation, physician_slots, 'morning', start_date + timedelta(days=single))
            df_list.append(available_time_slots.sample(n=1))
            available_time_slots = _find_available_time_slots(df, operation, physician_slots, 'evening', start_date + timedelta(days=single))
            df_list.append(available_time_slots.sample(n=1))
        dataframe = pd.concat(df_list, ignore_index=True)
        return dataframe


def get_time_slots_schedule(df):
    time_slots = []
    for index, row in df.iterrows():
        datetime_value = row['Date']  # Replace 'datetime_column' with the actual column name in your DataFrame
        timeslot_value = row['Available Slots'][0]  # Replace 'timeslot_column' with the actual column name in your DataFrame
        combined_slot = f"{datetime_value} {timeslot_value}"
        #combined_slot = timeslot_value
        time_slots.append(combined_slot)
    return time_slots

data = [[date(2023, 6, 1), '8:00 Am', 'DXLF'], [date(2023, 6, 1), '8:04 Am', 'DXLF'], [date(2023, 6, 1), '11:50 Am', 'PNS'], 
    [date(2023, 6, 1), '10:00 Am', 'DXLF'],
    [date(2023, 6, 2), '8:00 Am', 'DXLF'],[date(2023, 6, 1), '8:50 Am', 'DXLF'],[date(2023, 6, 1), '8:20 Am', 'DXLF'],
    [date(2023, 6, 3), '8:00 Am', 'DXLF'],[date(2023, 6, 3), '8:10 Am', 'DXLF'],[date(2023, 6, 3), '8:20 Am', 'DXLF'],
    [date(2023, 6, 3), '10:00 Am', 'DXLF'],[date(2023, 6, 3), '10:10 Am', 'DXLF'],[date(2023, 6, 3), '11:50 Am', 'PNS'],
    [date(2023, 6, 1), '8:20 Am', 'DXLF'],[date(2023, 6, 1), '8:30 Am', 'DXLF'],[date(2023, 6, 1), '8:40 Am', 'DXLF']]

# Create the pandas DataFrame
df = pd.DataFrame(data, columns = ['Date', 'Time','Procedure'])

df_final = available_appointments(df, 'DXLF', 5)

print(df_final)