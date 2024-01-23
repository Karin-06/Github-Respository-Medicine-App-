import streamlit as st
from datetime import datetime, timedelta
from streamlit_calendar import calendar

# Initialize medications and calendar events in session state
if 'medications' not in st.session_state:
    st.session_state.medications = {}

if 'calendar_events' not in st.session_state:
    st.session_state.calendar_events = []

# Define calendar options
calendar_options = {
    "headerToolbar": {
        "left": "today prev,next",
        "center": "title",
        "right": "resourceTimelineDay,resourceTimelineWeek,resourceTimelineMonth",
    },
    "slotMinTime": "06:00:00",
    "slotMaxTime": "18:00:00",
    "initialView": "resourceTimelineDay",
    "resourceGroupField": "Medication",
    "resources": [
        {"id": "medication", "title": "Medication"},
    ],
}

# Custom CSS for the calendar
custom_css = """
    .fc-event-past {
        opacity: 0.8;
    }
    .fc-event-time {
        font-style: italic;
    }
    .fc-event-title {
        font-weight: 700;
    }
    .fc-toolbar-title {
        font-size: 2rem;
    }
"""

# Function to add a new medication
def add_medication(name, dose, frequency):
    st.session_state.medications[name] = {'dose': dose, 'frequency': frequency, 'next_reminder': None}

# Function to display current medications
def display_medications():
    st.subheader('Current Medications')
    for name, details in st.session_state.medications.items():
        st.write(f"Name: {name}, Dose: {details['dose']}, Frequency: {details['frequency']}")

# Function to set a reminder for a medication and add it to the calendar
def set_reminder(name):
    if name in st.session_state.medications:
        dose = st.session_state.medications[name]['dose']
        frequency = st.session_state.medications[name]['frequency']

        now = datetime.now()
        next_reminder = now + timedelta(minutes=frequency)

        st.session_state.medications[name]['next_reminder'] = next_reminder
        formatted_datetime = next_reminder.strftime("%Y-%m-%d %H:%M:%S.%f")
        st.success(f"Reminder set for {name} at {formatted_datetime}")

        # Add the reminder as an event to the calendar
        st.session_state.calendar_events.append({
            "title": f"Take {name} ({dose})",
            "start": next_reminder.strftime("%Y-%m-%dT%H:%M:%S"),
            "end": (next_reminder + timedelta(minutes=15)).strftime("%Y-%m-%dT%H:%M:%S"),
            "resourceId": "medication",
        })

        # Display the updated calendar immediately
        calendar_component = calendar(
            events=st.session_state.calendar_events,
            options=calendar_options,
            custom_css=custom_css,
        )
        st.write(calendar_component)

    else:
        st.warning(f"Medication '{name}' not found. Please select a valid medication.")

# Streamlit app
st.title('Medication Reminder App')

# User input for adding a new medication
medication_name = st.text_input('Medication Name')
medication_dose = st.text_input('Dose')
medication_frequency = st.number_input('Frequency (in minutes)')

add_medication_button = st.button('Add Medication')
if add_medication_button:
    if medication_name and medication_dose and medication_frequency:
        add_medication(medication_name, medication_dose, medication_frequency)
        st.success(f'{medication_name} added successfully!')
    else:
        st.warning('Please fill in all fields.')

# Display current medications
display_medications()

# User input for setting a reminder
reminder_name = st.selectbox('Select a medication for a reminder', list(st.session_state.medications.keys()))

set_reminder_button = st.button('Set Reminder')
if set_reminder_button:
    if reminder_name:
        set_reminder(reminder_name)
    else:
        st.warning("Please select a medication before setting a reminder.")

# Display the initial calendar
st.write('Calendar')
calendar_component = calendar(
    events=st.session_state.calendar_events,
    options=calendar_options,
    custom_css=custom_css,
)
st.write(calendar_component)


