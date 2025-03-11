import streamlit as st
import json
import os
import time
from datetime import datetime

st.title('Papoy\'s Water List')

members = ['Benny', 'Lestat', 'Geo', 'Arjie', 'AU', 'Marven', 'Eyron', 'Lenar', 'Keanu']
state_file = 'state.json'

def load_state():
    if os.path.exists(state_file):
        with open(state_file, 'r') as f:
            return json.load(f)
    else:
        return {"buyers": members.copy(), "carry": members.copy()}

def save_state(state):
    with open(state_file, 'w') as f:
        json.dump(state, f)

state = load_state()

def check_if_buyer_reset():
    if not state['buyers']:
        state['buyers'] = members.copy()
        save_state(state)

def check_if_carry_reset():
    if not state['carry']:
        state['carry'] = members.copy()
        save_state(state)

# Periodically check for updates
def refresh_state():
    current_state = load_state()
    if current_state != state:
        st.rerun()

# Add a placeholder to periodically refresh the state
with st.form('myform'):
    check_if_buyer_reset()
    check_if_carry_reset()
    date = st.date_input('Date', value=datetime.now().date())
    name = st.pills('Buyer', state['buyers'], key="buyer_selectbox")
    quantity = st.number_input('Quantity', step=1)
    carry = st.pills('Carry', state['carry'], key="carry_selectbox")
    submit = st.form_submit_button('Submit')
    if submit:
        if name == None or carry == None:
            st.error("Please select a buyer and a carry")
        elif quantity <= 0:
            st.error("Quantity must be greater than 0")
        else:
            state['buyers'].remove(name)
            state['carry'].remove(carry)
            save_state(state)
            check_if_buyer_reset()
            check_if_carry_reset()
            st.rerun()

# Refresh the state every 5 seconds
while True:
    time.sleep(5)
    refresh_state()