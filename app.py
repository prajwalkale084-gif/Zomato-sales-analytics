import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(
    page_title="Zomato Performance Dashboard",
    layout="wide",
    initial_sidebar_state="expanded",
)

# File path
CSV_PATH = r"C:\Users\sus\Downloads\zomato pipeline\Data\Processed\zomato_master_cleaned.csv"

# Load dataset
df = pd.read_csv(CSV_PATH)
df.columns = df.columns.str.lower().str.strip()

# Automatically detect numeric column for revenue
possible_rev_cols = [
    col
    for col in df.columns
    if any(k in col for k in ["price", "amount", "cost", "total", "sales", "value"])
]

revenue_col = None
for col in possible_rev_cols:
    cleaned_series = pd.to_numeric(
        df[col].astype(str).str.replace(r"[^\d.]", "", regex=True),
        errors="coerce",
    )
    if cleaned_series.sum() > 0:
        df[col] = cleaned_series
        revenue_col = col
        break

st.title("🍕 Zomato Performance Dashboard")

if revenue_col:
    # Sidebar Filters
    st.sidebar.header("Filter Data")
    filtered_df = df.copy()

    # City Filter
    city_col = [c for c in df.columns if "city" in c]
    if city_col:
        selected_cities = st.sidebar.multiselect(
            "Select City",
            options=sorted(df[city_col[0]].dropna().unique()),
            default=sorted(df[city_col[0]].dropna().unique()),
        )
        filtered_df = filtered_df[filtered_df[city_col[0]].isin(selected_cities)]

    # Cuisine Filter
    if "cuisine" in df.columns:
        selected_cuisines = st.sidebar.multiselect(
            "Select Cuisine",
            options=sorted(df["cuisine"].dropna().unique()),
            default=sorted(df["cuisine"].dropna().unique()),
        )
        filtered_df = filtered_df[filtered_df["cuisine"].isin(selected_cuisines)]

    # Top KPI Metrics
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Revenue", f"₹{filtered_df[revenue_col].sum():,.2f}")
    col2.metric("Total Orders", f"{len(filtered_df):,}")
    col3.metric(
        "Average Order Value", f"₹{filtered_df[revenue_col].mean():,.2f}"
    )

    st.markdown("---")

    # Tabbed Layout
    tab1, tab2 = st.tabs(["📊 Analytics Overview", "📋 Raw Data & Export"])

    with tab1:
        c1, c2 = st.columns(2)
        with c1:
            if "cuisine" in filtered_df.columns:
                cuisine_df = (
                    filtered_df.groupby("cuisine")[revenue_col]
                    .sum()
                    .reset_index()
                    .sort_values(by=revenue_col, ascending=False)
                )
                fig1 = px.bar(
                    cuisine_df,
                    x="cuisine",
                    y=revenue_col,
                    title="Revenue by Cuisine",
                    labels={revenue_col: "Revenue (₹)", "cuisine": "Cuisine"},
                    color=revenue_col,
                    color_continuous_scale="Viridis",
                )
                st.plotly_chart(fig1, use_container_width=True)

        with c2:
            payment_col = [c for c in df.columns if "payment" in c]
            if payment_col:
                pay_df = (
                    filtered_df.groupby(payment_col[0])[revenue_col]
                    .sum()
                    .reset_index()
                )
                fig2 = px.pie(
                    pay_df,
                    values=revenue_col,
                    names=payment_col[0],
                    title="Revenue by Payment Method",
                    hole=0.4,
                )
                st.plotly_chart(fig2, use_container_width=True)

        rest_col = [c for c in df.columns if "restaurant" in c and "id" not in c and "city" not in c]
        if rest_col:
            top_rest = (
                filtered_df.groupby(rest_col[0])[revenue_col]
                .sum()
                .reset_index()
                .sort_values(by=revenue_col, ascending=True)
                .tail(10)
            )
            fig3 = px.bar(
                top_rest,
                x=revenue_col,
                y=rest_col[0],
                orientation="h",
                title="Top 10 Restaurants by Revenue",
                labels={revenue_col: "Revenue (₹)", rest_col[0]: "Restaurant"},
                color=revenue_col,
                color_continuous_scale="Plasma",
            )
            st.plotly_chart(fig3, use_container_width=True)

    with tab2:
        st.subheader("Filtered Dataset")
        st.dataframe(filtered_df, use_container_width=True)
        
        # Download Button
        csv_data = filtered_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Filtered Data as CSV",
            data=csv_data,
            file_name="zomato_filtered_data.csv",
            mime="text/csv",
        )
else:
    st.error("❌ Unable to calculate revenue automatically.")