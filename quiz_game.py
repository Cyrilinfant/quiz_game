import streamlit as st
import json
import logging

# Enable Streamlit logging
logging.basicConfig(level=logging.DEBUG)

# Load quiz data
def load_data():
    try:
        with open('data.json') as f:
            data = json.load(f)
        return data['question'], data['options'], data['answer']
    except Exception as e:
        logging.error("Error loading data: %s", e)
        st.error("There was an error loading the quiz data.")
        return [], [], []

questions, options, answers = load_data()

# Initialize session state variables if they don't exist
if 'q_no' not in st.session_state:
    st.session_state.q_no = 0
if 'correct' not in st.session_state:
    st.session_state.correct = 0
if 'selected' not in st.session_state:
    st.session_state.selected = -1
if 'show_result' not in st.session_state:
    st.session_state.show_result = False

# Display Title
st.markdown("<h1 style='text-align: center; color: #0073e6;'>🎮 Quiz Game</h1>", unsafe_allow_html=True)

# If quiz is finished
if st.session_state.q_no >= len(questions):
    st.session_state.show_result = True

# Display Result
if st.session_state.show_result:
    score = int(st.session_state.correct / len(questions) * 100)
    st.markdown(f'<h3 style="text-align: center; color: green;">🎉 Quiz Completed!<br>Score: {score}%<br>Correct: {st.session_state.correct}<br>Wrong: {len(questions) - st.session_state.correct}</h3>', unsafe_allow_html=True)
    if st.button("Restart", key="restart"):
        st.session_state.q_no = 0
        st.session_state.correct = 0
        st.session_state.selected = -1
        st.session_state.show_result = False
        st.experimental_rerun()
else:
    # Display current question
    st.markdown(f'<p style="font-size: 24px; font-weight: 600; color: #333;">{questions[st.session_state.q_no]}</p>', unsafe_allow_html=True)

    # Create two columns for options
    col1, col2 = st.columns(2)

    # Show options in columns
    with col1:
        for idx, option in enumerate(options[st.session_state.q_no][:2]):
            if st.button(option, key=f'option{idx}_left'):
                st.session_state.selected = idx
    with col2:
        for idx, option in enumerate(options[st.session_state.q_no][2:]):
            if st.button(option, key=f'option{idx}_right'):
                st.session_state.selected = idx + 2

    # On Next
    if st.session_state.selected != -1:
        correct_index = answers[st.session_state.q_no]
        if st.session_state.selected == correct_index:
            st.session_state.correct += 1
        st.session_state.q_no += 1
        st.session_state.selected = -1  # Reset for next question
        st.experimental_rerun()
