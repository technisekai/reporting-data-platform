import streamlit as st
from cores.generate_config import *
from dotenv import load_dotenv

load_dotenv()
st.title("Query Automation")
with st.form("configuration"):
    job_name = st.text_input("Job Name", "")
    team_name = st.text_input("Team Name", "")
    own_name = st.text_input("Your Name", "")
    cron_time = st.text_input("Cron Time", "")
    query = st.text_area(
        "Query",
        "",
    )
    destination_type_name = option = st.selectbox(
        "Destination Type Name",
        tuple(str(os.getenv('ui_list_destination_type')).split(',')),
    )
    destination_conn_name = option = st.selectbox(
        "Destination Connection Name",
        tuple(str(os.getenv('ui_list_destination_conn')).split(',')),
    )
    st.form_submit_button('Submit')

destination_config = {
    'destination_type_name': destination_type_name,
    'destination_conn_name': destination_conn_name
}
st.write(insert_config_to_database(
    connection='',
    job_name=job_name, 
    team_name=team_name,
    own_name=own_name,
    cron_time=cron_time, 
    query=query, 
    destination_config=destination_config
))