import pandas as pd
import streamlit as st
import requests

headers = {
"token": "webxjdlznb",
"Content-Type": "application/json"
}
response = requests.post(
    "https://smartchatapi.live/portal/Api/get_view_template",
    headers=headers
)
data = response.json()


st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Choose an option",
    [
        "Send Direct Message",
        "Send Multiple Messages",
        "Add Template"
    ]
)

st.title("testing")
if page == "Send Direct Message":
    sender = st.text_input("Sender WhatsApp Number")
    lst = []
    for i in data:
        lst.append(i['template_name'])
        
    template = st.selectbox("choose the template",lst)
    broadcast = st.text_input("Broadcast Name")
    media_url = st.text_input("Media URL (Optional)")
    param1 = st.text_input("Parameter 1")
    param2 = st.text_input("Parameter 2")

    if st.button("Send Template"):

        payload = {"sender_whatsapp_number":sender,
                "template_name":template,
                "broadcast_name":broadcast,
                "url":"",
                "parameter_value1":""}

        response = requests.post(
            "https://smartchatapi.live/portal/Api/send_template_message",   
            headers=headers,
            json=payload
        )

        st.write("Status Code:", response.status_code)

        try:
            data = response.json()
            st.write("Response:")
            st.json(data)
        except Exception:
            data = None
            st.write("Raw Response:")
            st.write(response.text)

        if response.status_code == 200:
            st.success("Message Sent!")
        else:
            st.error("Failed")

elif page == "Send Multiple Messages":
    sender = st.text_area("Sender WhatsApp Numbers (seperated by comma) ")
    lst = []
    for i in data:
        lst.append(i['template_name'])
        
    template = st.selectbox("choose the template",lst)
    broadcast = st.text_input("Broadcast Name")
    media_url = st.text_input("Media URL (Optional)")
    param1 = st.text_input("Parameter 1")
    param2 = st.text_input("Parameter 2")

    if st.button("Send Template"):

        payload = {"sender_whatsapp_number":sender,
                "template_name":template,
                "broadcast_name":broadcast,
                "url":"",
                "parameter_value1":""}

        response = requests.post(
            "https://smartchatapi.live/portal/Api/send_mutiple_number",   
            headers=headers,
            json=payload
        )

        st.write("Status Code:", response.status_code)

        try:
            data = response.json()
            st.write("Response:")
            st.json(data)
        except Exception:
            data = None
            st.write("Raw Response:")
            st.write(response.text)

        if response.status_code == 200:
            st.success("Message Sent!")
        else:
            st.error("Failed")

 