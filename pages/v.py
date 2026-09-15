import streamlit as st
import pandas as pd
from supabase import create_client

# -------------------------
# Supabase Connection
# -------------------------

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
SUPABASE_URL = "https://lbiioyctwrwxwwbnaewa.supabase.co"
SUPABASE_KEY = "sb_publishable_4ASf43j7RR3rE2c-DumiIg_4Tc5UvqH"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

response = supabase.table("companies").select("*").order("company_name").execute()

companies = response.data

if not companies:
    st.warning("No companies found.")
    st.stop()

df = pd.DataFrame(companies)

st.title("Company Directory")

search = st.text_input("Search Company")
f1, f2, f3, f4 = st.columns(4)

with f1:
    status_filter = st.selectbox(
        "Verification",
        ["All", "Verified", "Not Verified"]
    )

with f2:
    state_filter = st.selectbox(
        "State",
        ["All"] + sorted(df["state"].dropna().unique().tolist())
    )

with f3:
    city_filter = st.selectbox(
        "City",
        ["All"] + sorted(df["city"].dropna().unique().tolist())
    )

with f4:
    industry_filter = st.selectbox(
        "Industry",
        ["All"] + sorted(df["industry"].dropna().unique().tolist())
    )
filtered_df = df.copy()

# Search
if search:
    filtered_df = filtered_df[
        filtered_df["company_name"].str.contains(search, case=False, na=False)
    ]

# Verification
if status_filter != "All":
    filtered_df = filtered_df[
        filtered_df["verification_status"] == status_filter
    ]

# State
if state_filter != "All":
    filtered_df = filtered_df[
        filtered_df["state"] == state_filter
    ]

# City
if city_filter != "All":
    filtered_df = filtered_df[
        filtered_df["city"] == city_filter
    ]

# Industry
if industry_filter != "All":
    filtered_df = filtered_df[
        filtered_df["industry"] == industry_filter
    ]

for i in range(0, len(filtered_df), 2):

    col1, col2 = st.columns(2)

    # =========================================================
    # LEFT CARD
    # =========================================================

    with col1:

        row = filtered_df.iloc[i]

        with st.container(border=True):

            # Fixed content area
            c1, c2 = st.columns([4, 1])

            with c1:

                st.markdown(
                    f"""
                    <div style="
                        height:64px;
                        font-size:1.5rem;
                        font-weight:600;
                        line-height:1.3;
                        overflow:hidden;
                        display:flex;
                        align-items:flex-start;
                    ">
                        {row['company_name']}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                st.markdown(
                    f"""
                    <div style="height:30px; overflow:hidden; white-space:nowrap;
                                text-overflow:ellipsis;">
                        📧 {row['company_email']}
                    </div>

                    <div style="height:30px; overflow:hidden; white-space:nowrap;
                                text-overflow:ellipsis;">
                        📞 {row['company_phone']}
                    </div>

                    <div style="height:30px; overflow:hidden; white-space:nowrap;
                                text-overflow:ellipsis;">
                        📍 {row['city']}, {row['state']}
                    </div>

                    <div style="height:30px; overflow:hidden; white-space:nowrap;
                                text-overflow:ellipsis;">
                        🏭 {row['industry']}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            with c2:

                if row["verification_status"] == "Verified":
                    st.markdown(
                        """
                        <div style="
                            background:#d1fae5;
                            color:#065f46;
                            padding:6px 10px;
                            border-radius:15px;
                            text-align:center;
                            font-size:13px;
                            font-weight:600;
                            white-space:nowrap;">
                            ✓ Verified
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                else:
                    st.markdown(
                        """
                        <div style="
                            background:#f3f4f6;
                            color:#6b7280;
                            padding:6px 10px;
                            border-radius:15px;
                            text-align:center;
                            font-size:13px;
                            font-weight:600;
                            white-space:nowrap;">
                            Unverified
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

            # =================================================
            # FIXED SPACING BEFORE BUTTON
            # =================================================

            st.markdown(
                "<div style='height:100px'></div>",
                unsafe_allow_html=True
            )

            if st.button(
                "View →",
                key=f"view_{row['id']}",
                use_container_width=True
            ):
                st.session_state.company_id = row["id"]
                st.switch_page("pages/2_Company_Details.py")


    # =========================================================
    # RIGHT CARD
    # =========================================================

    if i + 1 < len(filtered_df):

        with col2:

            row = filtered_df.iloc[i + 1]

            with st.container(border=True):

                c1, c2 = st.columns([4, 1])

                with c1:

                    st.markdown(
                        f"""
                        <div style="
                            height:64px;
                            font-size:1.5rem;
                            font-weight:600;
                            line-height:1.3;
                            overflow:hidden;
                            display:flex;
                            align-items:flex-start;
                        ">
                            {row['company_name']}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                    st.markdown(
                        f"""
                        <div style="height:30px; overflow:hidden; white-space:nowrap;
                                    text-overflow:ellipsis;">
                            📧 {row['company_email']}
                        </div>

                        <div style="height:30px; overflow:hidden; white-space:nowrap;
                                    text-overflow:ellipsis;">
                            📞 {row['company_phone']}
                        </div>

                        <div style="height:30px; overflow:hidden; white-space:nowrap;
                                    text-overflow:ellipsis;">
                            📍 {row['city']}, {row['state']}
                        </div>

                        <div style="height:30px; overflow:hidden; white-space:nowrap;
                                    text-overflow:ellipsis;">
                            🏭 {row['industry']}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                with c2:

                    if row["verification_status"] == "Verified":
                        st.markdown(
                            """
                            <div style="
                                background:#d1fae5;
                                color:#065f46;
                                padding:6px 10px;
                                border-radius:15px;
                                text-align:center;
                                font-size:13px;
                                font-weight:600;
                                white-space:nowrap;">
                                ✓ Verified
                            </div>
                            """,
                            unsafe_allow_html=True
                        )

                    else:
                        st.markdown(
                            """
                            <div style="
                                background:#f3f4f6;
                                color:#6b7280;
                                padding:6px 10px;
                                border-radius:15px;
                                text-align:center;
                                font-size:13px;
                                font-weight:600;
                                white-space:nowrap;">
                                Unverified
                            </div>
                            """,
                            unsafe_allow_html=True
                        )

                # =================================================
                # SAME SPACING AS LEFT CARD
                # =================================================

                st.markdown(
                    "<div style='height:100px'></div>",
                    unsafe_allow_html=True
                )

                if st.button(
                    "View →",
                    key=f"view_{row['id']}",
                    use_container_width=True
                ):
                    st.session_state.company_id = row["id"]
                    st.switch_page("pages/2_Company_Details.py")