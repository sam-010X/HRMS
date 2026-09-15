import pandas as pd
import streamlit as st
import requests
from supabase import create_client


SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
#Company Name

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

industries = [
    "Administrative/Utilities - N - ADMINISTRATIVE AND SUPPORT SERVICE ACTIVITIES",
    "Agriculture - A - AGRICULTURE, FORESTRY AND FISHING",
    "Construction - F - CONSTRUCTION",
    "Education - P - EDUCATION",
    "Energy supply - D - ELECTRICITY, GAS, STEAM AND AIR CONDITIONING SUPPLY",
    "Entertainment - R - ARTS, ENTERTAINMENT AND RECREATION",
    "Extraterritorial - U - ACTIVITIES OF EXTRATERRITORIAL ORGANISATIONS AND BODIES",
    "Finance/Insurance - K - FINANCIAL AND INSURANCE ACTIVITIES",
    "Food/Hospitality - I - ACCOMMODATION AND FOOD SERVICE ACTIVITIES",
    "Health/Social - Q - HUMAN HEALTH AND SOCIAL WORK ACTIVITIES",
    "Households - T - ACTIVITIES OF HOUSEHOLDS AS EMPLOYERS; UNDIFFERENTIATED GOODS- AND SERVICES-PRODUCING ACTIVITIES OF HOUSEHOLDS FOR OWN USE",
    "IT/Communication - J - INFORMATION AND COMMUNICATION",
    "Manufacturing - C - MANUFACTURING",
    "Mining - B - MINING AND QUARRYING",
    "Other Services - S - OTHER SERVICE ACTIVITIES",
    "Public Administration - O - PUBLIC ADMINISTRATION AND DEFENCE; COMPULSORY SOCIAL SECURITY",
    "Real Estate - L - REAL ESTATE ACTIVITIES",
    "Scientific - M - PROFESSIONAL, SCIENTIFIC AND TECHNICAL ACTIVITIES",
    "Transportation/Logistics - H - TRANSPORTATION AND STORAGE",
    "Water supply - E - WATER SUPPLY; SEWERAGE, WASTE MANAGEMENT AND REMEDIATION ACTIVITIES",
    "Wholesale/Retail - G - WHOLESALE AND RETAIL TRADE; REPAIR OF MOTOR VEHICLES AND MOTORCYCLES"
]
import streamlit as st

st.set_page_config(
    page_title="Customer - Company",
    
    layout="wide"
)

st.title("Company details")
st.caption("Fill in the company details below.")



with st.form("company_form"):

    st.subheader("Basic Information")

    col1, col2 = st.columns(2)

    with col1:
        company_name = st.text_input(
            "Company Name",
            placeholder="e.g. ABC Technologies Pvt Ltd"
        )

        company_mail = st.text_input(
            "Company Email",
            placeholder="info@company.com"
        )

        company_no = st.text_input(
            "Phone Number",
            placeholder="+91 9876543210"
        )

        company_website = st.text_input(
            "Website",
            placeholder="https://company.com"
        )

        company_linkedin = st.text_input(
            "LinkedIn",
            placeholder="https://linkedin.com/company/..."
        )

    with col2:
        company_cin = st.text_input(
            "CIN",
            placeholder="L12345DL2024PLC123456"
        )

        company_tags = st.selectbox(
            "Verification",
            ["Verified", "Not Verified"]
        )

        company_salesperson = st.text_input(
            "Salesperson"
        )

        company_reference = st.text_input(
            "Reference"
        )

        company_industry = st.selectbox(
            "Industry",
            industries,
            index=None,
            placeholder="Select Industry"
        )

    st.divider()

    st.subheader("Address")

    company_add = st.text_input(
        "Street Address 1",
        placeholder="House No., Street"
    )
    
    company_add2 = st.text_input(
        "Street Address 2",
        placeholder="Area, Landmark (Optional)"
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        company_city = st.text_input(
            "City"
        )

    with col2:
        company_state = st.selectbox(
            "State",
            states
        )

    with col3:
        company_zip = st.text_input(
            "ZIP Code"
        )

    company_country = st.text_input(
        "Country",
        value="India"
    )

    st.divider()

    st.subheader("Additional Information")

    company_remarks = st.text_area(
        "Remarks",
        height=120,
        placeholder="Write any notes here..."
    )
    st.markdown("""
<style>

/* FORM SUBMIT BUTTON */
div[data-testid="stFormSubmitButton"] button {
    background: linear-gradient(135deg, #15803d, #22c55e, #4ade80) !important;
    background-size: 200% 200% !important;
    color: white !important;
    border-radius: 14px !important;
    border: none !important;
    font-weight: 700 !important;
    transition: all .35s ease !important;
}


/* Gradient animation + hover */
div[data-testid="stFormSubmitButton"] button:hover {
    background-position: right center !important;
    transform: translateY(-3px) !important;
    box-shadow: 0 8px 25px rgba(34,197,94,.55) !important;
}


/* Click effect */
div[data-testid="stFormSubmitButton"] button:active {
    transform: scale(0.97) !important;
}

</style>
""", unsafe_allow_html=True)
    submitted = st.form_submit_button(
        "Company Added",
        width="stretch"
    )

if submitted:
    
    data = {
        "company_name": company_name,
        "company_email": company_mail,
        "company_phone": company_no,
        "company_website": company_website,
        "company_linkedin": company_linkedin,
        "company_cin": company_cin,
        "verification_status": company_tags,
        "salesperson": company_salesperson,
        "reference": company_reference,
        "industry": company_industry,
        "street_address_1": company_add,
        "street_address_2": company_add2,
        "city": company_city,
        "state": company_state,
        "zip_code": company_zip,
        "country": company_country,
        "remarks": company_remarks,
    }
    try:
        response = supabase.table("companies").insert(data).execute()

        st.success("Company added successfully!")
        st.write(response.data)

    except Exception as e:
        st.error(f"Error: {e}")
