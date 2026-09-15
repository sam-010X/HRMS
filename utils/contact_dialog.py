
import streamlit as st
import requests
from datetime import datetime
from supabase import create_client 


SUPABASE_URL = "https://lbiioyctwrwxwwbnaewa.supabase.co"
SUPABASE_KEY = "sb_publishable_4ASf43j7RR3rE2c-DumiIg_4Tc5UvqH"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

designations = [
    "Chairman",
    "Vice Chairman",
    "Managing Director (MD)",
    "Whole-time Director",
    "Executive Director",
    "Non-Executive Director",
    "Independent Director",
    "Nominee Director",
    "Additional Director",
    "Alternate Director",

    "Chief Executive Officer (CEO)",
    "Chief Operating Officer (COO)",
    "Chief Financial Officer (CFO)",
    "Chief Technology Officer (CTO)",
    "Chief Information Officer (CIO)",
    "Chief Marketing Officer (CMO)",
    "Chief Human Resources Officer (CHRO)",
    "Chief Product Officer (CPO)",
    "Chief Compliance Officer (CCO)",
    "Company Secretary",

    "President",
    "Vice President",
    "General Manager",
    "Senior Manager",
    "Manager",
    "Assistant Manager",

    "Team Lead",
    "Project Manager",
    "Business Development Manager",
    "Sales Manager",
    "HR Manager",
    "Finance Manager",
    "Operations Manager",
    "Marketing Manager",
    "IT Manager",

    "Software Engineer",
    "Senior Software Engineer",
    "Data Scientist",
    "Business Analyst",
    "Consultant",

    "Partner",
    "Founder",
    "Co-Founder",
    "Owner",

    "Other"
]

states = [
    "Andhra Pradesh",
    "Arunachal Pradesh",
    "Assam",
    "Bihar",
    "Chhattisgarh",
    "Goa",
    "Gujarat",
    "Haryana",
    "Himachal Pradesh",
    "Jharkhand",
    "Karnataka",
    "Kerala",
    "Madhya Pradesh",
    "Maharashtra",
    "Manipur",
    "Meghalaya",
    "Mizoram",
    "Nagaland",
    "Odisha",
    "Punjab",
    "Rajasthan",
    "Sikkim",
    "Tamil Nadu",
    "Telangana",
    "Tripura",
    "Uttar Pradesh",
    "Uttarakhand",
    "West Bengal",
    "Andaman and Nicobar Islands",
    "Chandigarh",
    "Dadra and Nagar Haveli and Daman and Diu",
    "Delhi",
    "Jammu and Kashmir",
    "Ladakh",
    "Lakshadweep",
    "Puducherry"
]
@st.dialog("Edit Contact", width="medium")
def edit_contact(contact,
    supabase):

        with st.form(f"edit_contact_{contact['id']}"):

            name = st.text_input("Name", value=contact.get("name", ""))
            email = st.text_input("Email", value=contact.get("email", ""))
            phone = st.text_input("Phone", value=contact.get("phone", ""))
            linkedin = st.text_input("LinkedIn", value=contact.get("linkedin", ""))

            din = st.text_input("DIN", value=contact.get("din", ""))
            department = st.text_input("Department", value=contact.get("department", ""))

            designation = st.selectbox(
                "Designation",
                designations,
                index=designations.index(contact["designation"])
                if contact.get("designation") in designations else 0
            )

            salesperson = st.text_input(
                "Salesperson",
                value=contact.get("salesperson", "")
            )

            street1 = st.text_input(
                "Street Address 1",
                value=contact.get("street_address_1", "")
            )

            street2 = st.text_input(
                "Street Address 2",
                value=contact.get("street_address_2", "")
            )

            city = st.text_input("City", value=contact.get("city", ""))

            state = st.selectbox(
                "State",
                states,
                index=states.index(contact["state"])
                if contact.get("state") in states else 0
            )

            zip_code = st.text_input(
                "ZIP Code",
                value=contact.get("zip_code", "")
            )

            country = st.text_input(
                "Country",
                value=contact.get("country", "")
            )

            reference = st.text_input(
                "Reference",
                value=contact.get("reference", "")
            )

            notes = st.text_area(
                "Notes",
                value=contact.get("notes", "")
            )

            remarks = st.text_area(
                "Remarks",
                value=contact.get("remarks", "")
            )

            tags = st.selectbox("Tags",["Verified","Not Verified"],
                index=0 if contact.get("tags") == "Verified" else 1
            )

            if st.form_submit_button("Update Contact", use_container_width=True):

                supabase.table("company_contacts").update({
                    "name": name,
                    "email": email,
                    "phone": phone,
                    "linkedin": linkedin,
                    "din": din,
                    "designation": designation,
                    "department": department,
                    "salesperson": salesperson,
                    "street_address_1": street1,
                    "street_address_2": street2,
                    "city": city,
                    "state": state,
                    "zip_code": zip_code,
                    "country": country,
                    "reference": reference,
                    "notes": notes,
                    "remarks": remarks,
                    "tags": tags
                }).eq("id", contact["id"]).execute()

                st.success("Updated Successfully")
                st.rerun()


@st.dialog("👤 Contact Details", width="medium")
def show_contact(contact):

    st.subheader(contact["name"])

    din = contact.get("din")

    company_rows = []

    if din is not None:
        din = str(din).strip()

        company_response = (
            supabase
            .table("visual_table")
            .select("*")
            .eq("din", din)
            .execute()
        )

        company_rows = company_response.data or []

    tab1, tab2, tab3, tab4 = st.tabs(
        ["General", "Address", "Additional", "Company"]
    )

    with tab1:

        col1, col2 = st.columns(2)

        with col1:
            st.write("**Email**")
            st.write(contact.get("email") or "-")

            st.write("**Phone**")
            st.write(contact.get("phone") or "-")

            st.write("**LinkedIn**")
            st.write(contact.get("linkedin") or "-")

        with col2:
            st.write("**DIN**")
            st.write(contact.get("din") or "-")

            st.write("**Designation**")
            st.write(contact.get("designation") or "-")

            st.write("**Department**")
            st.write(contact.get("department") or "-")

    with tab2:

        st.write("**Street Address 1**")
        st.write(contact.get("street_address_1") or "-")

        st.write("**Street Address 2**")
        st.write(contact.get("street_address_2") or "-")

        c1, c2, c3 = st.columns(3)

        with c1:
            st.write("**City**")
            st.write(contact.get("city") or "-")

        with c2:
            st.write("**State**")
            st.write(contact.get("state") or "-")

        with c3:
            st.write("**ZIP Code**")
            st.write(contact.get("zip_code") or "-")

        st.write("**Country**")
        st.write(contact.get("country") or "-")

    with tab3:

        st.write("**Salesperson**")
        st.write(contact.get("salesperson") or "-")

        st.write("**Reference**")
        st.write(contact.get("reference") or "-")

        st.write("**Notes**")
        st.info(contact.get("notes") or "No notes")

        st.write("**Remarks**")
        st.info(contact.get("remarks") or "No remarks")

    with tab4:

        st.write(f"**DIN:** {din or '-'}")

        if not company_rows:
            st.info("No companies found for this DIN.")
        else:
            st.write(f"**Companies:** {len(company_rows)}")

            for row in company_rows:

                company_name = row.get("company_name") or "-"

                st.markdown(
                    f"""
                    <div style="
                        padding: 10px 14px;
                        margin-bottom: 8px;
                        border: 1px solid #ddd;
                        border-radius: 8px;
                    ">
                        <strong>{company_name}</strong>
                    </div>
                    """,
                    unsafe_allow_html=True
                )


@st.dialog("Whatsapp Message", width="medium")
def whastapp(contact,company_name):
    SUPABASE_URL = "https://lbiioyctwrwxwwbnaewa.supabase.co"
    SUPABASE_KEY = "sb_publishable_4ASf43j7RR3rE2c-DumiIg_4Tc5UvqH"

    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)    

    
    tab1, tab2 = st.tabs(["WhatsApp", "Whatsapp Tracker"])
    with tab1:
        headers = {
        "token": "webxjdlznb",
        "Content-Type": "application/json"
        }
        response = requests.post(
            "https://smartchatapi.live/portal/Api/get_view_template",
            headers=headers
        )
        data = response.json()
        sender = st.text_input("Sender WhatsApp Number",value = contact.get("phone"))
        lst = []
        for i in data:
            if i['template_status']=='APPROVED':
                lst.append(i['template_name'])
            
        template = st.selectbox("choose the template",lst)



        response = (
    supabase
    .table("broadcast_names")
    .select("id, broadcast_name")
    .order("broadcast_name")
    .execute()
)       
        options = [x["broadcast_name"] for x in response.data]
        options.append("➕ Add new...")

        selected_broadcast = st.selectbox("Broadcast Name", options)

        if selected_broadcast == "➕ Add new...":
            new_name = st.text_input("New broadcast name")

            if st.button("Add"):
                new_name = new_name.strip()

                if new_name and new_name not in options:
                    supabase.table("broadcast_names").insert({
                        "broadcast_name": new_name
                    }).execute()
                    selected_broadcast = new_name
        
        
        for templates in data:
            if templates['template_name']==template:
                template_header = templates['template_header']
                template_media_path = templates['template_header_file_path']
                break
        if template_header== 'MEDIA':
            media_url = st.text_input("Media URL (Optional)",value=template_media_path)
        else:
            media_url = ""
        param1 = st.text_input("Parameter 1")
        param2 = st.text_input("Parameter 2")
        
        if st.button("Send Template",use_container_width=True):

            payload = {"sender_whatsapp_number":sender,
                    "template_name":template,
                    "broadcast_name":selected_broadcast,
                    "url":media_url,
                    "parameter_value1":param1
                    }
            st.write(media_url)
            response = requests.post(
                "https://smartchatapi.live/portal/Api/send_template_message",   
                headers=headers,
                json=payload
            )

            st.write("Status Code:", response.status_code)

            try:
                data1 = response.json()
                st.write("Response:")
                st.json(data1)
            except Exception:
                data1 = None
                st.write("Raw Response:")
                st.write(response.text)

            if response.status_code == 200:
                st.success("Message Sent!")
                data1 = {
                        "contact_id": contact["id"],

                        "name": contact.get("name"),
                        "phone_number": contact.get("phone"),


                        "template_name": template,
                        "sent_at":datetime.now().isoformat(),
                        "Broadcast_name":selected_broadcast
                        }
                
                supabase.table("whatsapp_message_logs").insert(data1).execute()
            else:
                st.error("Failed")
    with tab2:
        logs = (
    supabase
    .table("whatsapp_message_logs")
    .select("*")
    .execute()
).data

        logs = [
            row for row in logs
            if str(row["phone_number"])[-10:] == str(sender)[-10:]
        ]

        st.subheader("WhatsApp History")

        if not logs:
            st.info("No messages found.")

        for idx, log in enumerate(logs):

            sent_at = datetime.fromisoformat(
                str(log["sent_at"]).replace("Z", "+00:00")
            )
            formatted_time = sent_at.strftime("%d %b %Y • %I:%M %p")

            with st.container(border=True):

                col1, col2 = st.columns([4, 2])

                with col1:
                    st.markdown(f"**📄 {log['template_name']}**")
                    st.caption(f"👤 {log['name']} • 📞 {log['phone_number']}")
                    

                with col2:
                    st.caption(formatted_time)
                    status = str(log["Read_status"]).upper()

                    if status == "SENT":
                        color = "#2196F3"
                    elif status == "DELIVERED":
                        color = "#FFC107"
                    elif status == "READ":
                        color = "#11FF00"
                    elif status in ("", "NONE", "NULL"):
                        color = "#808080"
                    else:
                        color = "#FD0505"

                    st.markdown(
                        f"""
                        <span style="
                            background-color: {color};
                            color: white;
                            padding: 4px 10px;
                            border-radius: 12px;
                            font-size: 12px;
                            font-weight: 600;
                        ">
                            {status}
                        </span>
                        """,
                        unsafe_allow_html=True
                    )

                # Template Preview
                with st.expander("📱 View Template"):

                    selected_template = None

                    for t in data:
                        if t["template_name"] == log["template_name"]:
                            selected_template = t
                            break

                    if selected_template:

                        # Header
                        if selected_template["template_header"] == "MEDIA":
                            st.image(
    selected_template["template_header_file_path"],
    width=250
)

                        # Body
                        st.markdown(selected_template["template_body"])

                        # Footer
                        if selected_template["template_footer"]:
                            st.caption(selected_template["template_footer"])

                        st.divider()

                        # CTA Buttons (Preview Only)
                        if selected_template["button_type"] == "Call to action":

                            col1, col2 = st.columns(2)

                            with col1:
                                if selected_template["First_button_name"]:
                                    st.button(
                                        "📅 Free Consultation",
                                        disabled=True,
                                        key=f"cta1_{idx}"
                                    )

                            with col2:
                                if selected_template["Second_button_name"]:
                                    st.button(
                                        f"📞 {selected_template['Second_button_name']}",
                                        disabled=True,
                                        key=f"cta2_{idx}"
                                    )

                    else:
                        st.warning("Template not found.")