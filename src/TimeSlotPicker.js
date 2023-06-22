import React from 'react';

const TimeSlotPicker = ({ timeSlots, onSelect }) => {
  return (
    <div>
      <h2>Select a Time Slot:</h2>
      <div className="time-slot-buttons">
        {timeSlots.map((timeSlot) => (
          <button
            key={timeSlot}
            className="time-slot-button"
            onClick={() => onSelect(timeSlot)}
          >
            {timeSlot}
          </button>
        ))}
      </div>
    </div>
  );
};

export default TimeSlotPicker;


