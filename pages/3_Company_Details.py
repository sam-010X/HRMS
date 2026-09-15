import streamlit as st
from supabase import create_client
from utils.contact_dialog import edit_contact,show_contact,whastapp
import base64
st.markdown("""
<style>

/* DETAILS BUTTON */
div[data-testid="stButton"] button[kind="secondary"] {
    background: linear-gradient(135deg, #2563eb, #06b6d4) !important;
    color: white !important;
    border-radius: 7px !important;
    border: none !important;
    font-weight: 700 !important;
    transition: all .25s ease !important;
}

div[data-testid="stButton"] button[kind="secondary"]:hover {
    transform: translateY(-3px);
    box-shadow: 0 8px 20px rgba(6,182,212,.5);
}


/* EDIT BUTTON */
div[data-testid="stButton"] button[kind="primary"] {
    background: linear-gradient(135deg, #9333ea, #ec4899) !important;
    color: white !important;
    border-radius: 7px !important;
    border: none !important;
    font-weight: 700 !important;
    transition: all .25s ease !important;
}

div[data-testid="stButton"] button[kind="primary"]:hover {
    transform: translateY(-3px);
    box-shadow: 0 8px 20px rgba(236,72,153,.5);
}
div[data-testid="stButton"] button[kind="tertiary"] {
    background: linear-gradient(135deg, #16a34a, #25D366) !important;
    color: white !important;
    border: none !important;
    border-radius: 7px !important;
    font-weight: 700 !important;
    transition: all .25s ease !important;
}

div[data-testid="stButton"] button[kind="tertiary"]:hover {
    background: linear-gradient(135deg, #128C7E, #25D366) !important;
    transform: translateY(-3px) !important;
    box-shadow: 0 8px 20px rgba(37, 211, 102, .45) !important;
}
</style>
""", unsafe_allow_html=True)

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

st.set_page_config(
    page_title="Company Details",
    layout="wide"
)


SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]


supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# --------------------------------------------------
# CSS
# --------------------------------------------------

st.markdown("""
<style>

.block-container{
    padding-top:2rem;
    padding-bottom:2rem;
}

.label{
    font-size:14px;
    color:gray;
    margin-bottom:2px;
}

.value{
    font-size:17px;
    font-weight:600;
    margin-bottom:18px;
}

</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# GET COMPANY
# --------------------------------------------------

company_id = st.session_state.get("company_id")

if company_id is None:
    st.error("No company selected.")
    st.stop()

response = (
    supabase.table("companies")
    .select("*")
    .eq("id", company_id)
    .single()
    .execute()
)

company = response.data

if company is None:
    st.error("Company not found.")
    st.stop()

# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.write("Current directory:", os.getcwd())
st.write("Files:", os.listdir("."))
st.write("Pages:", os.listdir("pages"))
c1, c2, c3 = st.columns([1,6,1])

with c1:
    if st.button("⬅ Back"):
        st.switch_page("pages/2_View_companies.py")

with c2:
    st.markdown(f"# {company['company_name']}")

with c3:
    if company["verification_status"] == "Verified":
        st.success("Verified")
    else:
        st.warning("Not Verified")

st.divider()

# --------------------------------------------------
# SUMMARY
# --------------------------------------------------
c1, c2, c3, c4 = st.columns(4)

with c1:
    st.caption("Industry")
    st.write(company.get("industry") or "-")

with c2:
    st.caption("City")
    st.write(company.get("city") or "-")

with c3:
    st.caption("State")
    st.write(company.get("state") or "-")

with c4:
    st.caption("Country")
    st.write(company.get("country") or "-")
st.divider()

# --------------------------------------------------
# TABS
# --------------------------------------------------

general,address,crm,remarks = st.tabs([
    "General",
    "Address",
    "CRM",
    "Remarks"
])

# --------------------------------------------------
# GENERAL
# --------------------------------------------------

with general:

    left,right = st.columns(2)

    with left:

        st.markdown('<div class="label">Company Name</div>',unsafe_allow_html=True)
        st.markdown(f'<div class="value">{company.get("company_name") or "-"}</div>',unsafe_allow_html=True)

        st.markdown('<div class="label">Email</div>',unsafe_allow_html=True)
        st.markdown(f'<div class="value">{company.get("company_email") or "-"}</div>',unsafe_allow_html=True)

        st.markdown('<div class="label">Phone</div>',unsafe_allow_html=True)
        st.markdown(f'<div class="value">{company.get("company_phone") or "-"}</div>',unsafe_allow_html=True)

        st.markdown('<div class="label">Website</div>',unsafe_allow_html=True)
        st.markdown(f'<div class="value">{company.get("company_website") or "-"}</div>',unsafe_allow_html=True)

    with right:

        st.markdown('<div class="label">LinkedIn</div>',unsafe_allow_html=True)
        st.markdown(f'<div class="value">{company.get("company_linkedin") or "-"}</div>',unsafe_allow_html=True)

        st.markdown('<div class="label">Industry</div>',unsafe_allow_html=True)
        st.markdown(f'<div class="value">{company.get("industry") or "-"}</div>',unsafe_allow_html=True)

        st.markdown('<div class="label">CIN</div>',unsafe_allow_html=True)
        st.markdown(f'<div class="value">{company.get("company_cin") or "-"}</div>',unsafe_allow_html=True)

        st.markdown('<div class="label">Verification</div>',unsafe_allow_html=True)
        st.markdown(f'<div class="value">{company.get("verification_status") or "-"}</div>',unsafe_allow_html=True)

with address:

    left,right = st.columns(2)

    with left:

        st.markdown('<div class="label">Street Address 1</div>',unsafe_allow_html=True)
        st.markdown(f'<div class="value">{company.get("street_address_1") or "-"}</div>',unsafe_allow_html=True)

        st.markdown('<div class="label">Street Address 2</div>',unsafe_allow_html=True)
        st.markdown(f'<div class="value">{company.get("street_address_2") or "-"}</div>',unsafe_allow_html=True)

        st.markdown('<div class="label">City</div>',unsafe_allow_html=True)
        st.markdown(f'<div class="value">{company.get("city") or "-"}</div>',unsafe_allow_html=True)

    with right:

        st.markdown('<div class="label">State</div>',unsafe_allow_html=True)
        st.markdown(f'<div class="value">{company.get("state") or "-"}</div>',unsafe_allow_html=True)

        st.markdown('<div class="label">ZIP Code</div>',unsafe_allow_html=True)
        st.markdown(f'<div class="value">{company.get("zip_code") or "-"}</div>',unsafe_allow_html=True)

        st.markdown('<div class="label">Country</div>',unsafe_allow_html=True)
        st.markdown(f'<div class="value">{company.get("country") or "-"}</div>',unsafe_allow_html=True)

# --------------------------------------------------
# CRM
# --------------------------------------------------

with crm:

    left,right = st.columns(2)

    with left:

        st.markdown('<div class="label">Salesperson</div>',unsafe_allow_html=True)
        st.markdown(f'<div class="value">{company.get("salesperson") or "-"}</div>',unsafe_allow_html=True)

    with right:

        st.markdown('<div class="label">Reference</div>',unsafe_allow_html=True)
        st.markdown(f'<div class="value">{company.get("reference") or "-"}</div>',unsafe_allow_html=True)

# --------------------------------------------------
# REMARKS
# --------------------------------------------------

with remarks:

    st.info(company.get("remarks") or "No remarks available.")


st.divider()

st.markdown("""
<style>
.action-card {
    background-color: #f8fafc;
    border: 1px solid #e5e7eb;
    border-radius: 12px;
    padding: 18px;
}
.action-title {
    font-size: 18px;
    font-weight: 600;
}
.action-desc {
    color: #6b7280;
    font-size: 14px;
}
</style>
""", unsafe_allow_html=True)


st.markdown(
    f"""
    <div class="action-card">
        <div class="action-title">
            👤 Add to Contacts
        </div>
        <div class="action-desc">
            Create a contact profile for {company.get('company_name')} and manage communication details.
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

st.write("")

col1, col2, col3 = st.columns([3,1,3])

with col2:
    
    @st.dialog("Add Director", width="medium")
    def add_director():
        st.markdown(
                    '<p style="color:red; font-size:12px; margin-top:-10px;">'
                    'If the director is not present, create a new director. Duplicate individuals cannot be added.'
                    '</p>',
                    unsafe_allow_html=True
                    )
        st.subheader("Basic Information")

        col1, col2 = st.columns(2)

        with col1:
            @st.cache_data(ttl=300)
            def get_directors():
                contacts = []
                start = 0
                batch_size = 500

                while True:
                    response = (
                        supabase
                        .table("company_contacts")
                        .select("id,name,din")
                        .range(start, start + batch_size - 1)
                        .execute()
                    )

                    data = response.data or []

                    if not data:
                        break

                    contacts.extend(data)

                    if len(data) < batch_size:
                        break

                    start += batch_size

                return contacts


            contacts = get_directors()

            names = list(dict.fromkeys(
                contact["name"]
                for contact in contacts
                if contact.get("name")
            ))
            
            selected_name = st.selectbox(
                "Name",
                [""] + names,
                format_func=lambda x: "Select Director" if not x else x,
                key="director_name"
            )
            new_name = st.text_input("Name")
            email = st.text_input(
                "Email",
                placeholder="example@email.com"
            )

            phone = st.text_input(
                "Phone",
                placeholder="+91 XXXXX XXXXX"
            )
            
            linkedin = st.text_input(
                "LinkedIn Profile"
            )

            tags = st.selectbox(
                "Tags",
                ["Verified", "Not Verified"]
            )

        with col2:
            
            if selected_name:
                selected_dins = list(dict.fromkeys(
                    contact.get("din")
                    for contact in contacts
                    if contact.get("name") == selected_name
                    and contact.get("din")
                ))

                if selected_dins:
                    din = st.selectbox(
                        "DIN",
                        selected_dins,
                        key="director_din"
                    )
                else:
                    din = st.selectbox(
                        "DIN",
                        [""],
                        format_func=lambda x: "No DIN found",
                        key="director_din"
                    )
            else:
                din = st.selectbox(
                    "DIN",
                    [""],
                    format_func=lambda x: "Select a name first",
                    key="director_din"
                )
            
            new_din = st.text_input("DIN",placeholder="00000000")
            department = st.text_input("Department")

            designation = st.selectbox(
                "Designation",
                designations
            )

            salesperson = st.text_input("Salesperson")

        with st.form("director_form"):

            st.divider()
            st.subheader("Address")

            street1 = st.text_input("Street Address 1")
            street2 = st.text_input("Street Address 2")

            col1, col2, col3 = st.columns(3)

            with col1:
                city = st.text_input("City")

            with col2:
                state = st.selectbox("State", states)

            with col3:
                zip_code = st.text_input("ZIP")

            country = st.text_input(
                "Country",
                value="India"
            )

            st.divider()
            st.subheader("Additional")

            reference = st.text_input("Reference")
            notes = st.text_area("Notes")
            remarks = st.text_area("Remarks")

            submit = st.form_submit_button(
                "Save Director",
                use_container_width=True
            )

        if submit:

            name_value = new_name.strip()
            din_value = new_din.strip()

            if not name_value:
                st.warning("Cannot add contact: Name is required.")
                return

            if not din_value:
                st.warning("Cannot add contact: DIN is required.")
                return

            existing_din = (
                supabase
                .table("company_contacts")
                .select("id,name,din")
                .eq("din", din_value)
                .execute()
            )

            if existing_din.data:
                st.warning(
                    f"Cannot add contact: DIN {din_value} already exists."
                )
                return

            phone_value = phone.strip()[-10:]

            existing_phone_number = (
                supabase
                .table("company_contacts")
                .select("id,name,din,phone")
                .eq("phone", phone_value)
                .execute()
            )

            if existing_phone_number.data:
                st.warning(
                    f"Cannot add contact: Phone number {phone_value} already exists."
                )
                return

            data = {
                
                "name": name_value,
                "email": email,
                "phone": phone,
                "street_address_1": street1,
                "street_address_2": street2,
                "city": city,
                "state": state,
                "zip_code": zip_code,
                "country": country,
                "din": din_value,
                "designation": designation,
                "department": department,
                "linkedin": linkedin,
                "salesperson": salesperson,
                "reference": reference,
                "notes": notes,
                "remarks": remarks
            }

            try:
                supabase.table("company_contacts").insert(data).execute()

                data2 = {
                    "company_name": company.get("company_name"),
                    "din": din_value,
                    "director_name": name_value
                }

                supabase.table("visual_table").insert(data2).execute()

                st.success(f"{name_value} added successfully!")
                st.cache_data.clear()
                st.rerun()

            except Exception as e:
                st.error(f"Error saving director: {e}")
    if st.button("Add Director"):
        add_director()
        
st.divider()
st.header("Company Contacts")

pages = st.selectbox("Pages:", [25, 50, 100, 200])

PAGE_SIZE = pages

if "contact_page" not in st.session_state:
    st.session_state.contact_page = 0

if st.session_state.get("contact_company_name") != company["company_name"]:
    st.session_state.contact_page = 0
    st.session_state.contact_company_name = company["company_name"]

page = st.session_state.contact_page

start = page * PAGE_SIZE
end = start + PAGE_SIZE - 1


# Find DINs for this company from visual_table
visual_response = (
    supabase
    .table("visual_table")
    .select("din")
    .eq("company_name", company["company_name"])
    .execute()
)

dins = [
    str(row["din"]).strip()
    for row in (visual_response.data or [])
    if row.get("din") is not None
]


# Find contacts using DIN
if dins:
    response = (
        supabase
        .table("company_contacts")
        .select("*", count="exact")
        .in_("din", dins)
        .range(start, end)
        .execute()
    )

    contacts = response.data or []
    total_contacts = response.count or 0
else:
    contacts = []
    total_contacts = 0


if not contacts:

    st.info("No contacts added yet.")

else:

    st.markdown("""
    <style>

    div[data-testid="stVerticalBlockBorderWrapper"] {
        border-radius: 18px !important;
        border: 1px solid rgba(128,128,128,0.20) !important;
        padding: 10px 12px !important;
        margin-bottom: 16px !important;
        transition: all 0.25s ease !important;
    }

    div[data-testid="stVerticalBlockBorderWrapper"]:hover {
        transform: translateY(-3px);
        border-color: rgba(37,99,235,0.35) !important;
        box-shadow: 0 8px 24px rgba(0,0,0,0.08) !important;
    }

    </style>
    """, unsafe_allow_html=True)

    for contact in contacts:

        with st.container(border=True):

            c1, c2, c3 = st.columns([5, 2, 2])

            with c1:

                if contact.get("tags") == "Verified":
                    badge = '<span style="background:#d1fae5;color:#065f46;padding:3px 10px;border-radius:15px;font-size:12px;font-weight:600;margin-left:8px;">✓ Verified</span>'
                else:
                    badge = '<span style="background:#f3f4f6;color:#6b7280;padding:3px 10px;border-radius:15px;font-size:12px;font-weight:600;margin-left:8px;">Unverified</span>'

                html = (
                    '<div style="font-size:18px;font-weight:600;">'
                    + (contact.get("name") or "-")
                    + " "
                    + badge
                    + "</div>"
                    + f'<div style="color:#6b7280;">{contact.get("designation") or "-"} • {contact.get("department") or "-"}</div>'
                    + f'<div>📧 {contact.get("email") or "-"}</div>'
                    + f'<div>📞 {contact.get("phone") or "-"}</div>'
                )

                st.markdown(html, unsafe_allow_html=True)

            with c2:

                st.caption("Location")

                st.write(
                    f"{contact.get('city') or '-'}, "
                    f"{contact.get('state') or '-'}"
                )

            with c3:

                b1, b2 = st.columns(2)

                with b1:

                    if st.button(
                        "Details",
                        key=f"details_{contact['id']}",
                        use_container_width=True
                    ):
                        show_contact(contact)

                with b2:

                    if st.button(
                        "Edit",
                        key=f"edit_{contact['id']}",
                        use_container_width=True
                    ):
                        edit_contact(contact, supabase)

                if st.button(
                    "WhatsApp",
                    icon=":material/chat:",
                    key=f"whatsapp_{contact['id']}",
                    type="tertiary",
                    use_container_width=True
                ):
                    whastapp(
                        contact,
                        company.get("company_name")
                    )


    if total_contacts > PAGE_SIZE:

        total_pages = (
            total_contacts + PAGE_SIZE - 1
        ) // PAGE_SIZE

        st.divider()

        col1, col2, col3 = st.columns([1, 2, 1])

        with col1:

            if st.button(
                "← Previous",
                disabled=page == 0,
                use_container_width=True
            ):
                st.session_state.contact_page -= 1
                st.rerun()

        with col2:

            st.markdown(
                f"""
                <div style="text-align:center; padding-top:8px;">
                    Page <b>{page + 1}</b> of <b>{total_pages}</b>
                    &nbsp; • &nbsp;
                    {total_contacts} contacts
                </div>
                """,
                unsafe_allow_html=True
            )

        with col3:

            if st.button(
                "Next →",
                disabled=page >= total_pages - 1,
                use_container_width=True
            ):
                st.session_state.contact_page += 1
                st.rerun()

        st.divider()
