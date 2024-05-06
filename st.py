import streamlit as st
import json

st.set_page_config("Employee tracker", page_icon='👤')

with open('employee_status.json', 'r') as f:
    statuses = dict(json.load(f))

    is_in = []
    is_out = []

for key in statuses.keys():
    if statuses[key] is True:
        is_in.append(key) 
    else:
        is_out.append(key)

for key in is_in:
    st.markdown(f"🟩 **{key}**: Checked-IN")

for key in is_out:
    st.markdown(f"🟥 **{key}**: Checked-OUT")

if st.button("🔄 Check again", use_container_width=True):
    st.rerun()