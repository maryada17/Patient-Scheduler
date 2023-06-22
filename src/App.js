import './App.css';
import React, { useEffect, useState } from 'react';
import axios from 'axios';
import TimeSlotPicker from './TimeSlotPicker';

const App = () => {
  const [timeSlots, setTimeSlots] = useState([]);
  const [selectedTimeSlot, setSelectedTimeSlot] = useState(null);

  useEffect(() => {
    fetchTimeSlots();
  }, []);

  const fetchTimeSlots = async () => {
    try {
      const response = await axios.get('http://127.0.0.1:8000/api/get-time-slots');
      setTimeSlots(response.data.timeSlots);
    } catch (error) {
      console.error('Error fetching time slots:', error);
    }
  };

  const handleTimeSlotSelect = (timeSlot) => {
    setSelectedTimeSlot(timeSlot);
  };

  const handleFormSubmit = async () => {
    try {
      await axios.post('http://127.0.0.1:8000/api/select-time-slot', { time_slot: selectedTimeSlot });
      console.log('Time slot selected successfully!');
    } catch (error) {
      console.error('Error selecting time slot:', error);
    }
  };

  return (
    <div className="app-container">
      <h1>Patient Appointment Time Slot Selection</h1>
      {timeSlots.length > 0 ? (
        <>
          <TimeSlotPicker timeSlots={timeSlots} onSelect={handleTimeSlotSelect} />
          <div className="submit-button-container">
          <button onClick={handleFormSubmit} disabled={!selectedTimeSlot}>
            Submit
          </button>
          </div>
        </>
      ) : (
        <p>Loading time slots...</p>
      )}
    </div>
  );
};

export default App;
