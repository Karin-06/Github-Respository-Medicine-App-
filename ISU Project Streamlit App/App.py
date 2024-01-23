import streamlit as st
import pytesseract
from PIL import Image
import time 
from streamlit_option_menu import option_menu

st.set_page_config(
    page_title="medication App",
    page_icon="💊",
    layout="wide",
    initial_sidebar_state="expanded"
)

#Inserting an image 

st.title('Medication App')
st.write("In this app you can extract text from your medication as well as set reminder and track your pills and Symptoms!")

# This creates navigation menu using streamlit's option menu to allow the user to select between different options (pill tracker, symptom tracker, and the reminder)
selected = option_menu(
    menu_title=None,
    options = ["Pill Tracker", "Symptom Tracker", "Calendar"],
    icons = ["calendar2-week-fill", "capsule-pill", "heart-pulse-fill"], #icons using Bootstrap Icons
    orientation = "horizontal",
    styles={
        "icon": {"color": "thistle", "font-size": "25px"}, 
        "nav-link": {"font-size": "15px", "text-align": "left", "margin":"2px", "--hover-color": "#eee"},
        "nav-link-selected": {"background-color": "lavender"},
    }
 )

# Calendar Page 
from datetime import datetime, timedelta
from streamlit_calendar import calendar

if selected=="Calendar":              #Display calender is calender selected 
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
    "slotMinTime": "00:00:00",
    "slotMaxTime": "24:00:00",
    "initialView": "resourceTimelineDay",
    "resourceGroupField": "Medication",
    "resources": [
        {"id": "medication", "title": "Medication"},
    ],
    "eventColor": "#D8BFD8"
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
        font-size: 14px
        colour: #333
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
        print("Calendar Events Before: ", st.session_state.calendar_events)
        calendar_component = calendar(
            events=st.session_state.calendar_events,
            options=calendar_options,
            custom_css=custom_css,
        )
        st.write(calendar_component)
        print("Calendar Events After:", st.session_state.calendar_events)

    else:
        st.warning(f"Medication '{name}' not found. Please select a valid medication.")

# Visualization / Putting image to the side of the text 
 col1, col2 = st.columns([3,1])
 with col1:
  st.write(" ")
  st.header('Medication Reminder App')
 with col2: 
  st.image('Calender_image.png', width = 130)
 

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

pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

with st.sidebar: 
 def organize_text_into_sections(text):
    # Define keywords that indicate the start of a section
    section_keywords = ["Active Ingredients", "Uses", "Warnings", "Directions", "Other information", "Questions?", "Questions or comments?", "Do not use", "Inactive ingredients", "Allergy alert", "Warning", "Use"]

    sections = {}
    current_section = None

    lines = text.split('\n')

    # Iterate through the lines
    for line in lines:
        # Check if the line contains any of the section keywords
        for keyword in section_keywords:
            if keyword in line:
                current_section = keyword
                sections[current_section] = []
                break
        # If we are in a section, add the line to the current section
        if current_section is not None:
            sections[current_section].append(line)

    # Convert the sections to a more readable format (e.g., strings)
    organized_sections = {section: '\n'.join(lines) for section, lines in sections.items()}

    return organized_sections

 def format_bullet_points(text):
    lines = text.split('\n')
    formatted_text = ""

    for line in lines:
        # Check if the line starts with a common bullet point character
        if line.strip().startswith(("m @", "@", "m@","e ", "=")):
            # Add bullet point formatting
            formatted_text += f"- {line}\n"
        else:
            formatted_text += line + "\n"

    return formatted_text

# Streamlit app

 st.title("Medicine Label Analyzer") #Adding title
 st.text("Upload an image containing English Text")
 col1 = st.columns([1])

# section for user to upload the image 
 upload_image = st.file_uploader('Choose an image for conversion', type=["jpg", "png", "jpeg"])

 if upload_image is not None:
     progress_text = "Operation in progress. Please wait."

     img = Image.open(upload_image)
     st.image(upload_image)

     if st.button("Extract Text"):
        st.write("Extracted Text")
        output_text = pytesseract.image_to_string(img)
        
        # Format bullet points
        formatted_output = format_bullet_points(output_text)
        
        # Remove 'all the weird output and replace it with space'
        formatted_output = formatted_output.replace('m@', '')
        formatted_output = formatted_output.replace('m @', '')
        formatted_output = formatted_output.replace('@', '')
        formatted_output = formatted_output.replace('e ', '')
        formatted_output = formatted_output.replace('=', '')
        
        # Organize and display text in sections
        organized_sections = organize_text_into_sections(formatted_output)
        for section, content in organized_sections.items():
            with st.expander(section):
                st.write(content)

#__________________________________________________________________________________________________________________
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta

def load_data():
    try:
        pill_data = pd.read_csv('pill_data.csv')
    except FileNotFoundError:
        pill_data = pd.DataFrame(columns=['Pill Name', 'Time', 'Date'])

    try:
        symptom_data = pd.read_csv('symptom_data.csv')
    except FileNotFoundError:
        symptom_data = pd.DataFrame(columns=['Date', 'Symptoms/Feelings', 'emotion'])

    return pill_data, symptom_data

# Function to save data to file
def save_data(pill_data, symptom_data):
    pill_data.to_csv('pill_data.csv', index=False)
    symptom_data.to_csv('symptom_data.csv', index=False)

# Function to resample data based on user selection
def resample_data(data, interval):
    if interval == 'Day':
        return data.resample('D').size()
    elif interval == 'Hour':
        return data.resample('H').size()
    elif interval == 'Month':
        return data.resample('M').size()

# Load data at the beginning of the app
pill_data, symptom_data = load_data()

 #Displaying toast message  
def display_pill_message(): 
  msg = st.toast("Updating")        
  time.sleep(1)
  msg.toast('Good Job for tracking your pill!', icon = "👍")

# Pill Tracker
if selected == "Pill Tracker":
 col1, col2 = st.columns([3,1])
 with col1:
  st.write("")
  st.header('Pill Tracker')
 with col2: 
  st.image('Image_of_cat.png', width = 130)

 pill_name = st.text_input('Enter Pill Name:', key='pill_name')
 pill_time = st.time_input('Select Time to Take Pill:', key='pill_time')
 pill_date = st.date_input('Select Date to Take Pill:', key='pill_date')

 if st.button('Track Pill'):
    new_pill_entry = pd.DataFrame({'Pill Name': [pill_name],
                                   'Time': [pill_time.strftime('%H:%M')],
                                   'Date': [pill_date.strftime('%Y-%m-%d')]})
    pill_data = pd.concat([pill_data, new_pill_entry], ignore_index=True)
    display_pill_message()
    st.success('Pill tracked successfully!')
    st.dataframe(pill_data)


# Delete Pill Entry
 st.subheader('Delete Pill Entry')
 delete_pill_index = st.number_input('Enter the index to delete a pill entry:', min_value=0, max_value=max(0, len(pill_data)-1), step=1, key='delete_pill_index')
 if st.button('Delete Pill Entry') and not pill_data.empty:
    pill_data = pill_data.drop(index=delete_pill_index).reset_index(drop=True)
    st.success('Pill entry deleted successfully.')

# Fixed interval for pill intake visualization
 selected_interval_pill = 'Day'

# Show a line chart of pill intake over time
 st.header('Pill Intake Over Time')
 if not pill_data.empty:
    pill_data['Date'] = pd.to_datetime(pill_data['Date'])
    
    # Resample the data based on the fixed interval
    resampled_data_pill = resample_data(pill_data.groupby('Date').size(), selected_interval_pill)
    
    # Plot the resampled pill intake data with customized colors and font
    fig_pill, ax_pill = plt.subplots(figsize=(10, 6))
    sns.lineplot(x=resampled_data_pill.index, y=resampled_data_pill.values, marker='o', color="#D8BFD8", ax=ax_pill)
    plt.title(f'Pill Intake Over Time ({selected_interval_pill}ly)', color="#2c3e50")

    plt.xlabel('Date', color="#2c3e50")
    plt.ylabel('Number of Pills', color="#2c3e50")

    # Place the year on top of the graph
    ax_pill.xaxis.tick_top()
    ax_pill.xaxis.set_label_position('top')

    st.pyplot(fig_pill)

if selected == "Symptom Tracker": 
 #Displaying toast message 
 def display_symptom_message(): 
  msg = st.toast("Updating")           #displaying message 
  time.sleep(1)
  msg.toast('Good Job for tracking your symptoms!', icon = "👍")

# Symptom and Feeling Tracker
# To display title and the image 
 col1, col2 = st.columns([3,1])
 with col1:
   st.write(" ")
   st.header('Symptom/Feeling Tracker')
 with col2: 
   st.image('feeling_image.png', width = 130)

#Option menu for teh emotion 
 col3, col4 = st.columns([1,1])
 with col4: 
  selected2 = option_menu(
    menu_title=None,
    options = ["Excellent", "Good", "Moderate", "Unwell"],
    icons = ["emoji-laughing-fill", "emoji-smile-fill", "emoji-neutral-fill", "emoji-dizzy-fill"],
        styles={
        "icon": {"color": "thistle", "font-size": "16px"}, 
        "nav-link": {"font-size": "18px", "text-align": "left", "margin":"1px", "--hover-color": "#eee"},
        "nav-link-selected": {"background-color": "lavender"},
    }
 )

# User input about the info for date/symtpoms 
 with col3: 
  symptom_date = st.date_input('Select Date for Symptom/Feeling:', key='symptom_date')
  symptoms = st.text_area('Enter Symptoms/Feelings:', key='symptoms')

# adds the information to csv files
 if st.button('Track Symptoms/Feelings'):
    new_symptom_entry = pd.DataFrame({'Date': [symptom_date.strftime('%Y-%m-%d')],
                                      'Symptoms/Feelings': [symptoms], 'emotion':[selected2]})
    symptom_data = pd.concat([symptom_data, new_symptom_entry], ignore_index=True)
    display_symptom_message()
    st.success('Symptoms/Feelings tracked successfully!')
    st.dataframe(symptom_data)

# Delete Symptom Entry
 st.subheader('Delete Symptom Entry')
 delete_symptom_index = st.number_input('Enter the index to delete a symptom entry:', min_value=0, max_value=max(0, len(symptom_data)-1), step=1, key='delete_symptom_index')
 if st.button('Delete Symptom Entry') and not symptom_data.empty:
    symptom_data = symptom_data.drop(index=delete_symptom_index).reset_index(drop=True)
    st.success('Symptom entry deleted successfully.')

# Show a bar chart of symptom entries over time (fixed to daily interval)
 st.header('Symptom Entries Over Time (Daily)')
 if not symptom_data.empty:
    symptom_data['Date'] = pd.to_datetime(symptom_data['Date'])
    
    # Resample the data based on the daily interval
    resampled_data_symptom = resample_data(symptom_data.groupby('Date').size(), 'Day')
    
    #extract only the date (to make the grph more orgnaized)
    resampled_data_symptom.index = resampled_data_symptom.index.date

    # Plot the resampled symptom entry data with customized colors and font
    fig_symptom, ax_symptom = plt.subplots(figsize=(10, 6))
    sns.barplot(x=resampled_data_symptom.index, y=resampled_data_symptom.values, color='#D8BFD8', ax=ax_symptom)

    #make it so it only shows date for the x-axis 
   
    step_value = len(resampled_data_symptom) // 10
    tick_positions = range(10, len(resampled_data_symptom.index), 1 if step_value == 0 else step_value) #make sure that even the range is 0 the code still gets executed 

    tick_labels = [date.strftime('%Y-%m-%d') for date in resampled_data_symptom.index[tick_positions]]

    ax_symptom.set_xticks(tick_positions)
    ax_symptom.set_xticklabels(tick_labels, rotation=45)

    plt.title('Symptom Entries Over Time (Daily)', color='#2c3e50')
    plt.xlabel('Date', color='#2c3e50')
    plt.ylabel('Number of Entries', color='#2c3e50')
    st.pyplot(fig_symptom)

# Save data at the end of the app
save_data(pill_data, symptom_data)