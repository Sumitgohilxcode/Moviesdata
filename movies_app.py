import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# Page Config
st.set_page_config(
    page_title="🎬 Film & OTT Box Office Financial Dashboard (60k)",
    page_icon="🍿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling (Cinematic Dark / Crimson Theme)
st.markdown("""
    <style>
    .main { background-color: #0F0F12; }
    .stMetric {
        background-color: #1A1A22;
        padding: 15px;
        border-radius: 12px;
        border: 1px solid #2D2D3A;
    }
    div[data-testid="stMetricValue"] {
        font-size: 24px;
        font-weight: bold;
        color: #E50914;
    }
    h1, h2, h3 { color: #F5F5F7; }
    </style>
""", unsafe_allow_html=True)

@st.cache_data
def load_movie_data():
    file_path = "Movies_Financial_BoxOffice_Performance_60k.xlsx"
    try:
        df = pd.read_excel(file_path)
    except Exception:
        np.random.seed(42)
        n_rows = 60000
        movie_titles_prefix = ["The Last", "Shadow of", "Chronicles of", "Rise of", "Legend of", "Secret of", "Return to", "Beyond the", "Agent", "Operation"]
        movie_titles_core = ["Cyberpunk", "Valhalla", "Kingdom", "Gladiator", "Darkness", "Horizon", "Empire", "Dynasty", "Matrix", "Odyssey", "Infinity", "Phoenix"]
        movie_titles_suffix = ["Reborn", "Legacy", "Part 1", "Part 2", "Unchained", "Protocol", "Origins", "Endgame", "Vengeance", "Rising"]

        movie_names = [
            f"{np.random.choice(movie_titles_prefix)} {np.random.choice(movie_titles_core)} {np.random.choice(movie_titles_suffix)}"
            for _ in range(n_rows)
        ]

        genres = ["Action", "Sci-Fi", "Drama", "Comedy", "Thriller", "Horror", "Romance", "Animation", "Adventure"]
        languages = ["Hindi", "English", "Telugu", "Tamil", "Malayalam", "Kannada"]
        studios = ["YRF", "Dharma Productions", "Red Chillies", "T-Series", "Universal Pictures", "Warner Bros", "Marvel Studios", "Sun Pictures", "Mythri Movie Makers"]
        ott_platforms = ["Netflix", "Amazon Prime", "Disney+ Hotstar", "JioCinema", "SonyLIV", "ZEE5"]

        genre_col = np.random.choice(genres, size=n_rows)
        lang_col = np.random.choice(languages, size=n_rows)
        studio_col = np.random.choice(studios, size=n_rows)
        ott_col = np.random.choice(ott_platforms, size=n_rows)
        release_year = np.random.choice(range(2018, 2027), size=n_rows)

        prod_budget = np.round(np.random.uniform(15, 350, size=n_rows), 2)
        marketing_cost = np.round(prod_budget * np.random.uniform(0.15, 0.30, size=n_rows), 2)
        total_investment = np.round(prod_budget + marketing_cost, 2)

        box_office = np.round(total_investment * np.random.uniform(0.4, 3.5, size=n_rows), 2)
        ott_rights = np.round(total_investment * np.random.uniform(0.20, 0.45, size=n_rows), 2)
        satellite_music_rights = np.round(total_investment * np.random.uniform(0.10, 0.25, size=n_rows), 2)

        total_revenue = np.round(box_office + ott_rights + satellite_music_rights, 2)
        net_profit = np.round(total_revenue - total_investment, 2)
        roi_percent = np.round((net_profit / total_investment) * 100, 2)

        conditions = [
            (roi_percent >= 100),
            (roi_percent >= 30) & (roi_percent < 100),
            (roi_percent >= 0) & (roi_percent < 30),
            (roi_percent < 0)
        ]
        verdicts = ["Blockbuster", "Super Hit", "Average / Hit", "Flop"]
        verdict_col = np.select(conditions, verdicts, default="Flop")

        df = pd.DataFrame({
            "Movie ID": [f"MOV-{10000 + i}" for i in range(n_rows)],
            "Movie Title": movie_names,
            "Genre": genre_col,
            "Language": lang_col,
            "Production Studio": studio_col,
            "OTT Platform Rights": ott_col,
            "Release Year": release_year,
            "Production Budget (₹ Cr)": prod_budget,
            "Marketing Cost (₹ Cr)": marketing_cost,
            "Total Investment (₹ Cr)": total_investment,
            "Box Office Collection (₹ Cr)": box_office,
            "OTT Rights Revenue (₹ Cr)": ott_rights,
            "Satellite & Music Rights (₹ Cr)": satellite_music_rights,
            "Total Gross Revenue (₹ Cr)": total_revenue,
            "Net Profit / Loss (₹ Cr)": net_profit,
            "ROI (%)": roi_percent,
            "Box Office Verdict": verdict_col
        })
    return df

df = load_movie_data()

# Header
st.title("🎬 Box Office & OTT Financial Performance Dashboard")
st.caption("Executive Insights for 60,000 Movies Across Cinema Box Office, OTT Rights & Satellite Revenue.")
st.markdown("---")

# Sidebar Filters
st.sidebar.header("🍿 Movie Filters")
selected_genre = st.sidebar.multiselect("Select Genre", options=df["Genre"].unique(), default=df["Genre"].unique())
selected_lang = st.sidebar.multiselect("Select Language", options=df["Language"].unique(), default=df["Language"].unique())
selected_studio = st.sidebar.multiselect("Select Production Studio", options=df["Production Studio"].unique(), default=df["Production Studio"].unique()[:5])
selected_ott = st.sidebar.multiselect("Select OTT Platform", options=df["OTT Platform Rights"].unique(), default=df["OTT Platform Rights"].unique())

filtered_df = df[
    (df["Genre"].isin(selected_genre)) &
    (df["Language"].isin(selected_lang)) &
    (df["Production Studio"].isin(selected_studio)) &
    (df["OTT Platform Rights"].isin(selected_ott))
]

# Top KPI Summary
col1, col2, col3, col4, col5 = st.columns(5)
total_inv = filtered_df["Total Investment (₹ Cr)"].sum()
total_rev = filtered_df["Total Gross Revenue (₹ Cr)"].sum()
total_profit = filtered_df["Net Profit / Loss (₹ Cr)"].sum()
avg_roi = filtered_df["ROI (%)"].mean()
total_movies = len(filtered_df)

col1.metric("Total Investment", f"₹{total_inv/1000:.2f}K Cr")
col2.metric("Total Revenue", f"₹{total_rev/1000:.2f}K Cr")
col3.metric("Net Profit", f"₹{total_profit/1000:.2f}K Cr")
col4.metric("Average ROI", f"{avg_roi:.1f}%")
col5.metric("Movies Analyzed", f"{total_movies:,}")

st.markdown("---")

# Visualizations Row 1
c1, c2 = st.columns(2)

with c1:
    st.subheader("🎥 Box Office Verdict Breakdown")
    verdict_counts = filtered_df["Box Office Verdict"].value_counts().reset_index()
    fig1 = px.pie(
        verdict_counts, values="count", names="Box Office Verdict",
        hole=0.4, color="Box Office Verdict",
        color_discrete_map={"Blockbuster": "#10B981", "Super Hit": "#3B82F6", "Average / Hit": "#F59E0B", "Flop": "#EF4444"}
    )
    fig1.update_layout(template="plotly_dark", height=400)
    st.plotly_chart(fig1, use_container_width=True)

with c2:
    st.subheader("📊 Revenue Streams Comparison by Genre")
    genre_summary = filtered_df.groupby("Genre")[["Box Office Collection (₹ Cr)", "OTT Rights Revenue (₹ Cr)", "Satellite & Music Rights (₹ Cr)"]].sum().reset_index()
    fig2 = px.bar(
        genre_summary, x="Genre", y=["Box Office Collection (₹ Cr)", "OTT Rights Revenue (₹ Cr)", "Satellite & Music Rights (₹ Cr)"],
        barmode="stack", color_discrete_sequence=["#E50914", "#3B82F6", "#8B5CF6"]
    )
    fig2.update_layout(template="plotly_dark", height=400)
    st.plotly_chart(fig2, use_container_width=True)

# Visualizations Row 2
c3, c4 = st.columns(2)

with c3:
    st.subheader("📺 OTT Platform Monetization Share")
    ott_summary = filtered_df.groupby("OTT Platform Rights")["OTT Rights Revenue (₹ Cr)"].sum().reset_index()
    fig3 = px.bar(
        ott_summary, x="OTT Platform Rights", y="OTT Rights Revenue (₹ Cr)",
        color="OTT Platform Rights", color_discrete_sequence=px.colors.qualitative.Bold
    )
    fig3.update_layout(template="plotly_dark", height=400, showlegend=False)
    st.plotly_chart(fig3, use_container_width=True)

with c4:
    st.subheader("📈 Annual Industry Revenue Trend")
    trend_summary = filtered_df.groupby("Release Year")[["Total Investment (₹ Cr)", "Total Gross Revenue (₹ Cr)", "Net Profit / Loss (₹ Cr)"]].sum().reset_index()
    fig4 = px.line(
        trend_summary, x="Release Year", y=["Total Investment (₹ Cr)", "Total Gross Revenue (₹ Cr)", "Net Profit / Loss (₹ Cr)"],
        markers=True, color_discrete_sequence=["#EF4444", "#10B981", "#3B82F6"]
    )
    fig4.update_layout(template="plotly_dark", height=400)
    st.plotly_chart(fig4, use_container_width=True)

# Interactive Explorer
st.markdown("---")
st.subheader("🔍 Movie Financial Database (Top Filtered Records)")
st.dataframe(filtered_df.head(1000), use_container_width=True)
