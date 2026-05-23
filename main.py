import streamlit as st
import pandas as pd
from pathlib import Path
from modules.formater import Title, Footer
from modules.importer import DataImport

# --- PAGE CONFIGURATION ---
title = "🏠 Data Analyst Insights"
Title().page_config(title)
Footer().footer()

# --- ASSET LOADING ---
@st.cache_data(show_spinner=False)
def _read_css_file(css_path: Path) -> str:
    """Read the CSS file and cache it to avoid I/O on every rerender."""
    if css_path.exists():
        with open(css_path) as f:
            return f.read()
    return ""

def load_assets() -> None:
    """Load the custom CSS and background animations."""
    css_path = Path(__file__).parent / "assets" / "style.css"
    css_content = _read_css_file(css_path)
    if css_content:
        st.markdown(f"<style>{css_content}</style>", unsafe_allow_html=True)
    
    # Inject animated background elements defined in style.css
    st.markdown('<div class="grid-background"></div>', unsafe_allow_html=True)
    st.markdown('<div class="glow-orb glow-orb-1"></div>', unsafe_allow_html=True)
    st.markdown('<div class="glow-orb glow-orb-2"></div>', unsafe_allow_html=True)

# Load custom styles & fonts
load_assets()

# --- DATA PROCESSING FOR SUMMARY METRICS ---
@st.cache_data(ttl=60*60)
def get_summary_metrics():
    """Fetch database and compute live high-level metrics for the landing page."""
    try:
        jobs_all = DataImport().fetch_and_clean_data()
        
        # Calculate row count
        total_jobs = len(jobs_all)
        
        # Standardized Average Salary
        salary_data = jobs_all['salary_standardized'].dropna()
        avg_salary = int(salary_data.mean()) if not salary_data.empty else 0
        
        # Date range for consecutive days
        first_date = jobs_all.date_time.dt.date.min()
        last_date = jobs_all.date_time.dt.date.max()
        days_consecutive = (last_date - first_date).days
        
        return total_jobs, avg_salary, days_consecutive, first_date, last_date
    except Exception as e:
        return 0, 0, 0, "N/A", "N/A"

total_jobs, avg_salary, days_consecutive, first_date, last_date = get_summary_metrics()

# --- HERO SECTION ---
st.markdown(
    """
    <div class="hero">
        <h1 class="hero-title">
            <span class="hero-title-line">Google Jobs Analytics</span>
            <span class="hero-title-highlight">Data Analyst Market Control</span>
        </h1>
        <p class="hero-subtitle">
            An open-source interactive dashboard tracking daily job requirements, salary trends, and pipeline health for Aspiring Data Analysts in the United States.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

# --- SUMMARY METRICS SECTION ---
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(
        f"""
        <div class="metric-container">
            <div class="metric-value">{total_jobs:,}</div>
            <div class="metric-label">Job Postings</div>
            <div class="metric-subtext">Collected daily via SerpApi</div>
        </div>
        """,
        unsafe_allow_html=True
    )
with col2:
    st.markdown(
        f"""
        <div class="metric-container">
            <div class="metric-value">${avg_salary:,.0f}</div>
            <div class="metric-label">Avg Salary</div>
            <div class="metric-subtext">Standardized base annual salary</div>
        </div>
        """,
        unsafe_allow_html=True
    )
with col3:
    st.markdown(
        f"""
        <div class="metric-container">
            <div class="metric-value">{days_consecutive} Days</div>
            <div class="metric-label">Scraping Horizon</div>
            <div class="metric-subtext">From {first_date} to {last_date}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

# --- MODULES DIRECTORY SECTION ---
st.markdown(
    """
    <div class="section-header">
        <h2 class="section-header-title">🔍 Explore Dashboard Modules</h2>
        <p class="section-header-subtitle">Select a subpage in the sidebar navigation menu on the left to deep-dive into market statistics</p>
    </div>
    """,
    unsafe_allow_html=True
)

col_left, col_right = st.columns(2)

with col_left:
    st.markdown(
        """
        <div class="feature-card">
            <span class="feature-icon">🛠️</span>
            <h3 class="feature-title">Skills Analysis</h3>
            <p class="feature-desc">Discover the top skills (SQL, Python, Excel, Power BI) employers seek. Compare overall demand or track daily skill percentage fluctuations over time.</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(
        """
        <div class="feature-card">
            <span class="feature-icon">🏥</span>
            <h3 class="feature-title">Scraping Pipeline Health</h3>
            <p class="feature-desc">Audit the daily data collection pipeline. Track average volume collected per day, percent increase, database expansion rates, and date alignment.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

with col_right:
    st.markdown(
        """
        <div class="feature-card">
            <span class="feature-icon">💸</span>
            <h3 class="feature-title">Salary Insights</h3>
            <p class="feature-desc">Visualize salary histograms for Data Analysts. Sift through annual base pay, hourly rates, or standardized scales filtered by programming skills.</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(
        """
        <div class="feature-card">
            <span class="feature-icon">🌎</span>
            <h3 class="feature-title">Interactive Data Explorer</h3>
            <p class="feature-desc">Filter, sort, and search through the raw dataset. Build custom queries using search terms, location patterns, or job schedule categories.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

# Row 3 - About & Sidebar Info
col_about, col_guide = st.columns(2)
with col_about:
    st.markdown(
        """
        <div class="feature-card">
            <span class="feature-icon">📊</span>
            <h3 class="feature-title">About & Resources</h3>
            <p class="feature-desc">Learn about the project goal, resources used (SerpApi free search tier), Kaggle job postings dataset details, and link to GitHub and YouTube.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

with col_guide:
    st.markdown(
        """
        <div class="feature-card">
            <span class="feature-icon">🚀</span>
            <h3 class="feature-title">How to Begin</h3>
            <p class="feature-desc">Use the left sidebar navigation links to navigate between pages. Data filters on each subpage let you customize the charts dynamically.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

# --- SIDEBAR DESIGN ---
with st.sidebar:
    st.image("https://github.com/lukebarousse/Data_Analyst_Streamlit_App_V1/raw/main/images/luke_Favicon.png", width=70)
    st.markdown("### 📊 Market Control Center")
    st.caption("Google Search Job Analytics V1.0")
    st.markdown("---")
    st.info("💡 **Tips:** Select any page from the sidebar menu to explore charts. Filters on those pages will automatically slice the live data!")
