import streamlit as st
import pandas as pd
from supabase import create_client

st.set_page_config(
    page_title="WhatsApp Dashboard",
    
    layout="wide"
)


SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]


supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
@st.cache_data(ttl=300)
def get_total_companies():
    total = 0
    start = 0
    batch_size = 1000

    while True:
        response = (
            supabase
            .table("companies")
            .select("company_name")
            .range(start, start + batch_size - 1)
            .execute()
        )

        data = response.data or []

        if not data:
            break

        total += len({
            " ".join(c["company_name"].strip().split()).lower()
            for c in data
            if c.get("company_name")
        })

        if len(data) < batch_size:
            break

        start += batch_size

    return total

total_companies = get_total_companies()

@st.cache_data(ttl=300)
def get_contact_counts():
    unique_dins = set()
    unique_phones = set()
    unique_emails = set()
    unique_records = set()

    start = 0
    batch_size = 1000

    while True:
        response = (
            supabase
            .table("company_contacts")
            .select("id,din,phone,email")
            .range(start, start + batch_size - 1)
            .execute()
        )

        data = response.data or []

        if not data:
            break

        for contact in data:
            if contact.get("id"):
                unique_records.add(contact["id"])

            if contact.get("din"):
                unique_dins.add(contact["din"].strip().lower())

            if contact.get("phone"):
                unique_phones.add(contact["phone"].strip().lower())

            if contact.get("email"):
                unique_emails.add(contact["email"].strip().lower())

        if len(data) < batch_size:
            break

        start += batch_size

    return (
        len(unique_dins),
        len(unique_phones),
        len(unique_emails),
        len(unique_records)
    )



unique_dins, unique_phones, unique_emails, unique_records = get_contact_counts()

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Companies", total_companies)

with col2:
    st.metric("Unique Phone Numbers", unique_phones)

with col3:
    st.metric("Unique Email IDs", unique_emails)

with col4:
    st.metric("Total Unique individuals", unique_records)


@st.cache_data(ttl=300)
def get_industry_counts():
    industry_counts = {}
    start = 0
    batch_size = 5000

    while True:
        response = (
            supabase
            .table("companies")
            .select("industry")
            .range(start, start + batch_size - 1)
            .execute()
        )

        data = response.data or []

        if not data:
            break

        for company in data:
            industry = company.get("industry")

            if industry:
                industry = " ".join(industry.strip().split())
                if industry:
                    industry_counts[industry] = industry_counts.get(industry, 0) + 1

        if len(data) < batch_size:
            break

        start += batch_size

    return industry_counts


industry_counts = get_industry_counts()

industry_df = pd.DataFrame(
    list(industry_counts.items()),
    columns=["Industry", "Company Count"]
).sort_values("Company Count", ascending=False)

st.subheader("Companies by Industry")
st.dataframe(
    industry_df,
    use_container_width=True,
    hide_index=True
)

# st.title("WhatsApp Message Dashboard")

# data = (
#     supabase
#     .table("whatsapp_message_logs")
#     .select("*")
#     .execute()
#     .data
# )

# df = pd.DataFrame(data)

# if df.empty:
#     st.warning("No message data available.")
#     st.stop()

# df["sent_at"] = pd.to_datetime(
#     df["sent_at"],
#     errors="coerce"
# )

# df["Read_status"] = (
#     df["Read_status"]
#     .fillna("Unknown")
#     .astype(str)
#     .str.upper()
# )



# df["template_name"] = (
#     df["template_name"]
#     .fillna("Unknown")
#     .astype(str)
# )

# st.markdown("""
# <style>
# .metric-card {
#     padding: 20px;
#     border-radius: 12px;
#     background-color: #f7f7f7;
#     border: 1px solid #e5e5e5;
# }
# .metric-title {
#     font-size: 14px;
#     color: #666;
# }
# .metric-value {
#     font-size: 30px;
#     font-weight: 700;
# }
# </style>
# """, unsafe_allow_html=True)

# st.sidebar.header("Filters")


# templates = sorted(df["template_name"].unique())

# selected_templates = st.sidebar.multiselect(
#     "Template",
#     templates,
#     default=templates
# )

# statuses = sorted(df["Read_status"].unique())

# selected_statuses = st.sidebar.multiselect(
#     "Status",
#     statuses,
#     default=statuses
# )

# min_date = df["sent_at"].min().date()
# max_date = df["sent_at"].max().date()

# date_range = st.sidebar.date_input(
#     "Date Range",
#     value=(min_date, max_date),
#     min_value=min_date,
#     max_value=max_date
# )

# filtered = df[
    
#     df["template_name"].isin(selected_templates)
#     & df["Read_status"].isin(selected_statuses)
# ].copy()

# if len(date_range) == 2:
#     start_date, end_date = date_range

#     filtered = filtered[
#         (filtered["sent_at"].dt.date >= start_date)
#         & (filtered["sent_at"].dt.date <= end_date)
#     ]

# total_messages = len(filtered)

# unique_numbers = filtered["phone_number"].nunique()

# read_messages = len(
#     filtered[
#         filtered["Read_status"].isin(
#             ["READ", "DELIVERED"]
#         )
#     ]
# )

# unread_messages = len(
#     filtered[
#         filtered["Read_status"].isin(
#             ["UNREAD", "SENT", "PENDING"]
#         )
#     ]
# )

# st.markdown("### Overview")

# c1, c2, c3, c4 = st.columns(4)

# with c1:
#     st.metric(
#         "Total Messages",
#         f"{total_messages:,}"
#     )

# with c2:
#     st.metric(
#         "Unique Contacts",
#         f"{unique_numbers:,}"
#     )

# with c3:
#     st.metric(
#         "Read / Delivered",
#         f"{read_messages:,}"
#     )

# with c4:
#     st.metric(
#         "Unread / Pending",
#         f"{unread_messages:,}"
#     )

# st.divider()

# left, right = st.columns(2)

# with left:

#     st.subheader("📊 Messages by Status")

#     status_chart = (
#         filtered["Read_status"]
#         .value_counts()
#         .rename_axis("Status")
#         .reset_index(name="Messages")
#     )

#     st.bar_chart(
#         status_chart.set_index("Status")
#     )


# st.divider()

# left, right = st.columns(2)

# with left:

#     st.subheader("📨 Messages by Template")

#     template_chart = (
#         filtered["template_name"]
#         .value_counts()
#         .rename_axis("Template")
#         .reset_index(name="Messages")
#     )

#     st.bar_chart(
#         template_chart.set_index("Template")
#     )

# with right:

#     st.subheader("📅 Daily Message Activity")

#     daily = (
#         filtered
#         .set_index("sent_at")
#         .resample("D")
#         .size()
#         .rename("Messages")
#     )

#     st.line_chart(daily)

# st.divider()

# st.subheader("🕐 Recent Messages")

# recent = (
#     filtered
#     .sort_values("sent_at", ascending=False)
    
# )

# display_columns = ["name",
#     "phone_number",
#     "template_name",
#     "sent_at",
#     "Read_status"
# ]

# display_columns = [
#     c for c in display_columns
#     if c in recent.columns
# ]

# st.dataframe(
#     recent[display_columns],
#     use_container_width=True,
#     hide_index=True
# )
