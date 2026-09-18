import pandas as pd
import streamlit as st
from supabase import create_client
from utils.contact_dialog import show_contact,edit_contact
st.markdown("""
<style>

div[data-testid="stButton"] button[kind="secondary"] {
    background: linear-gradient(135deg, #2563eb, #06b6d4) !important;
    color: white !important;
    border-radius: 14px !important;
    border: none !important;
    font-weight: 700 !important;
    transition: all .25s ease !important;
}

div[data-testid="stButton"] button[kind="secondary"]:hover {
    transform: translateY(-3px);
    box-shadow: 0 8px 20px rgba(6,182,212,.5);
}

</style>
""", unsafe_allow_html=True)


SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]


supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

st.header("Company Contacts")
PAGE_SIZE = st.selectbox(
    "Contacts per page:",
    [25, 50, 100, 200]
)

references_response = (
    supabase
    .table("company_contacts")
    .select("reference")
    .execute()
)

references = sorted(
    {
        str(row["reference"]).strip()
        for row in (references_response.data or [])
        if row.get("reference") is not None
        and str(row["reference"]).strip()
    }
)

selected_reference = st.selectbox(
    "Reference",
    ["All"] + references,
    key="contact_reference_filter"
)

status_filter = st.selectbox(
    "Verification",
    ["All", "Verified", "Not Verified"],
    key="contact_verification_filter"
)
phone_filter = st.text_input(
    "Phone Number",
    placeholder="Search phone number...",
    key="contact_phone_filter"
)


if "contact_page" not in st.session_state:
    st.session_state.contact_page = 0

if "last_reference_filter" not in st.session_state:
    st.session_state.last_reference_filter = selected_reference

if "last_status_filter" not in st.session_state:
    st.session_state.last_status_filter = status_filter

if "last_phone_filter" not in st.session_state:
    st.session_state.last_phone_filter = phone_filter

if (
    selected_reference != st.session_state.last_reference_filter
    or status_filter != st.session_state.last_status_filter
    or phone_filter != st.session_state.last_phone_filter
):
    st.session_state.contact_page = 0
    st.session_state.last_reference_filter = selected_reference
    st.session_state.last_status_filter = status_filter
    st.session_state.last_phone_filter = phone_filter


page = st.session_state.contact_page

start = page * PAGE_SIZE
end = start + PAGE_SIZE - 1


query = (
    supabase
    .table("company_contacts")
    .select("*", count="exact")
    .order("name")
)

if selected_reference != "All":
    query = query.eq("reference", selected_reference)

if status_filter != "All":
    query = query.eq("tags", status_filter)

if phone_filter.strip():
    query = query.eq("phone", phone_filter.strip())
response = (
    query
    .range(start, end)
    .execute()
)

contacts = response.data or []
total_contacts = response.count or 0

if not contacts:
    st.info("No contacts found.")
    st.stop()


dins = [
    str(contact["din"]).strip()
    for contact in contacts
    if contact.get("din") is not None
]

visual_map = {}

if dins:
    visual_response = (
        supabase
        .table("visual_table")
        .select("din, company_name")
        .in_("din", dins)
        .execute()
    )

    for row in visual_response.data or []:
        if row.get("din") is not None:
            visual_map[str(row["din"]).strip()] = row.get("company_name", "-")


for contact in contacts:
    din = contact.get("din")

    if din is not None:
        din = str(din).strip()

    contact["company_name"] = visual_map.get(din, "-")

col1, col2, col3, col4, col5 = st.columns([4, 3, 3, 3, 2])

with col1:
    st.markdown("**Name**")

with col2:
    st.markdown("**Phone**")

with col3:
    st.markdown("**Email**")

with col4:
    st.markdown("**Reference**")

with col5:
    st.markdown("**Details**")


for index, contact in enumerate(contacts):

    col1, col2, col3, col4, col5 = st.columns([4, 3, 3, 3, 2])

    with col1:
        st.markdown(
            f'<div class="contact-row">{contact.get("name") or "-"}</div>',
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            f'<div class="contact-row">{contact.get("phone") or "-"}</div>',
            unsafe_allow_html=True
        )

    with col3:
        st.markdown(
            f'<div class="contact-row">{contact.get("email") or "-"}</div>',
            unsafe_allow_html=True
        )

    with col4:
        st.markdown(
            f'<div class="contact-row">{contact.get("reference") or "-"}</div>',
            unsafe_allow_html=True
        )

    with col5:
        if st.button(
            "Details",
            key=f"details_{contact['id']}_{page}_{index}",
            use_container_width=True
        ):
            show_contact(contact)

if total_contacts > PAGE_SIZE:

    total_pages = (total_contacts + PAGE_SIZE - 1) // PAGE_SIZE

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
                Page {page + 1} of {total_pages} • {total_contacts} contacts
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
