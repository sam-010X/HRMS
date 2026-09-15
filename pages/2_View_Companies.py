import streamlit as st
import pandas as pd
from supabase import create_client
import string
# -------------------------
# Supabase Connection
# -------------------------

PAGE_SIZE = 50
FETCH_SIZE = 1000
st.markdown("""
<style>

/* VIEW BUTTON */
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


st.title("Company Directory")

if "selected_letter" not in st.session_state:
    st.session_state.selected_letter = "A"

if "company_page" not in st.session_state:
    st.session_state.company_page = 0

if "last_search" not in st.session_state:
    st.session_state.last_search = ""

filter_options = ["#"] + list(string.ascii_uppercase)

cols = st.columns(13)

for i, letter in enumerate(filter_options):
    with cols[i % 13]:
        if st.button(
            letter,
            key=f"letter_{letter}",
            use_container_width=True,
            type=(
                "primary"
                if st.session_state.selected_letter == letter
                else "secondary"
            )
        ):
            st.session_state.selected_letter = letter
            st.session_state.company_page = 0
            st.rerun()

selected_letter = st.session_state.selected_letter

st.divider()

search = st.text_input(
    "Search Company",
    placeholder=f"Search {selected_letter} companies..."
).strip()

if search != st.session_state.last_search:
    st.session_state.company_page = 0
    st.session_state.last_search = search

try:

    query = (
        supabase
        .table("companies")
        .select("id, company_name")
        .order("company_name")
    )

    if selected_letter == "#":

        query = (
            query
            .gte("company_name", "0")
            .lt("company_name", "A")
        )

    else:

        start_letter = selected_letter

        if selected_letter == "Z":
            end_letter = "ZZZZZZZZZZ"
        else:
            end_letter = chr(ord(selected_letter) + 1)

        query = (
            query
            .gte("company_name", start_letter)
            .lt("company_name", end_letter)
        )

    all_companies = []

    offset = 0

    while True:

        response = (
            query
            .range(
                offset,
                offset + FETCH_SIZE - 1
            )
            .execute()
        )

        batch = response.data or []

        if not batch:
            break

        all_companies.extend(batch)

        if len(batch) < FETCH_SIZE:
            break

        offset += FETCH_SIZE

    companies = all_companies

except Exception as e:

    st.error("Supabase query failed.")
    st.code(str(e))
    st.stop()

if search:

    search_lower = search.lower()

    companies = [
        company
        for company in companies
        if search_lower in (
            company.get("company_name") or ""
        ).lower()
    ]

total_companies = len(companies)

st.subheader(f"{selected_letter} Companies")

if total_companies == 0:

    if search:
        st.info(
            f'No companies found matching "{search}".'
        )
    else:
        st.info(
            f"No companies found starting with {selected_letter}."
        )

    st.stop()

total_pages = max(
    1,
    (total_companies + PAGE_SIZE - 1) // PAGE_SIZE
)

if st.session_state.company_page >= total_pages:
    st.session_state.company_page = total_pages - 1
    st.rerun()

page = st.session_state.company_page

start = page * PAGE_SIZE
end = start + PAGE_SIZE

page_companies = companies[start:end]

st.caption(
    f"Showing {start + 1}–{min(end, total_companies)} "
    f"of {total_companies} companies"
)

for company in page_companies:

    col1, col2 = st.columns([6, 1])

    with col1:

        st.markdown(
            f"""
            <div class="company-name">
                {company.get("company_name", "")}
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:

        if st.button(
            "View →",
            key=f"view_{company['id']}",
            use_container_width=True
        ):

            st.session_state.company_id = company["id"]

            st.switch_page(
                "pages/3_Company_Details.py"
            )

st.divider()

col1, col2, col3 = st.columns([1, 2, 1])

with col1:

    if st.button(
        "← Previous",
        disabled=page == 0,
        use_container_width=True
    ):

        st.session_state.company_page -= 1
        st.rerun()

with col2:

    st.markdown(
        f"""
        <div style="
            text-align:center;
            font-weight:600;
            padding-top:8px;
        ">
            Page {page + 1} of {total_pages}
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

        st.session_state.company_page += 1
        st.rerun()
