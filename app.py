import streamlit as st
import pickle

# Initialize session state if not already done
if 'todo_list' not in st.session_state:
    st.session_state.todo_list = []

# Load existing to-do items from file
try:
    with open('todo_list.pkl', 'rb') as f:
        st.session_state.todo_list = pickle.load(f)
except FileNotFoundError:
    pass

# Function to save the to-do list to a file
def save_todo_list():
    with open('todo_list.pkl', 'wb') as f:
        pickle.dump(st.session_state.todo_list, f)

# Streamlit application
st.title('To-Do List Application')

# User input for adding new tasks
new_task = st.text_input('Add a new task')
if st.button('Add'):
    if new_task:
        st.session_state.todo_list.append(new_task)
        save_todo_list()  # Save to file after adding a task

# Display current to-do items
if st.session_state.todo_list:
    st.write('### My To-Do List')
    for task in st.session_state.todo_list:
        st.write('- ', task)
else:
    st.write('No tasks yet!')