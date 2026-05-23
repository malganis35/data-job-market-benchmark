import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
from modules.formater import Title, Footer
from modules.importer import DataImport

# Title page and footer
title = "🛠️ Skills"
t = Title().page_config(title)
f = Footer().footer()

# Import data
jobs_all = DataImport().fetch_and_clean_data()

# Dictionary for skills and tools mapping, in order to have a correct naming
keywords_skills = {
    'airflow': 'Airflow', 'alteryx': 'Alteryx', 'asp.net': 'ASP.NET', 'atlassian': 'Atlassian', 
    'excel': 'Excel', 'power_bi': 'Power BI', 'tableau': 'Tableau', 'srss': 'SRSS', 'word': 'Word', 
    'unix': 'Unix', 'vue': 'Vue', 'jquery': 'jQuery', 'linux/unix': 'Linux / Unix', 'seaborn': 'Seaborn', 
    'microstrategy': 'MicroStrategy', 'spss': 'SPSS', 'visio': 'Visio', 'gdpr': 'GDPR', 'ssrs': 'SSRS', 
    'spreadsheet': 'Spreadsheet', 'aws': 'AWS', 'hadoop': 'Hadoop', 'ssis': 'SSIS', 'linux': 'Linux', 
    'sap': 'SAP', 'powerpoint': 'PowerPoint', 'sharepoint': 'SharePoint', 'redshift': 'Redshift', 
    'snowflake': 'Snowflake', 'qlik': 'Qlik', 'cognos': 'Cognos', 'pandas': 'Pandas', 'spark': 'Spark', 'outlook': 'Outlook'
}

keywords_programming = {
    'sql' : 'SQL', 'python' : 'Python', 'r' : 'R', 'c':'C', 'c#':'C#', 'javascript' : 'JavaScript', 'js':'JS', 'java':'Java', 
    'scala':'Scala', 'sas' : 'SAS', 'matlab': 'MATLAB', 'c++' : 'C++', 'c/c++' : 'C / C++', 'perl' : 'Perl','go' : 'Go',
    'typescript' : 'TypeScript','bash':'Bash','html' : 'HTML','css' : 'CSS','php' : 'PHP','powershell' : 'Powershell',
    'rust' : 'Rust', 'kotlin' : 'Kotlin','ruby' : 'Ruby','dart' : 'Dart','assembly' :'Assembly',
    'swift' : 'Swift','vba' : 'VBA','lua' : 'Lua','groovy' : 'Groovy','delphi' : 'Delphi','objective-c' : 'Objective-C',
    'haskell' : 'Haskell','elixir' : 'Elixir','julia' : 'Julia','clojure': 'Clojure','solidity' : 'Solidity',
    'lisp' : 'Lisp','f#':'F#','fortran' : 'Fortran','erlang' : 'Erlang','apl' : 'APL','cobol' : 'COBOL',
    'ocaml': 'OCaml','crystal':'Crystal','javascript/typescript' : 'JavaScript / TypeScript','golang':'Golang',
    'nosql': 'NoSQL', 'mongodb' : 'MongoDB','t-sql' :'Transact-SQL', 'no-sql' : 'No-SQL','visual_basic' : 'Visual Basic',
    'pascal':'Pascal', 'mongo' : 'Mongo', 'pl/sql' : 'PL/SQL','sass' :'Sass', 'vb.net' : 'VB.NET','mssql' : 'MSSQL',
}

# Skill sort, count, and filter list data
def agg_skill_data(jobs_df):
    keywords_all = {**keywords_skills, **keywords_programming}
    # Explode the lists of tokens into individual rows (vectorized)
    exploded = jobs_df['description_tokens'].explode()
    # Strip whitespace
    cleaned_exploded = exploded.str.strip()
    # Map lowercase tokens to capitalized/correct keywords, keeping original if not found
    mapped_exploded = cleaned_exploded.str.lower().map(keywords_all).fillna(cleaned_exploded)
    # Count occurrences
    skill_data = mapped_exploded.value_counts().rename_axis('keywords').reset_index(name='counts')
    skill_data = skill_data[skill_data.keywords != '']
    skill_data['percentage'] = skill_data.counts / len(jobs_df)
    return skill_data


# Aggregate skills daily
def agg_skill_daily_data(jobs_df):
    jobs_df = jobs_df.copy()
    jobs_df['date'] = jobs_df.date_time.dt.date
    keywords_all = {**keywords_skills, **keywords_programming}
    
    # Explode the description tokens column and keep alignment with the date
    df_exploded = jobs_df[['date', 'description_tokens']].explode('description_tokens')
    df_exploded['description_tokens'] = df_exploded['description_tokens'].str.strip()
    
    # Map keywords vectorially
    df_exploded['keywords'] = df_exploded['description_tokens'].str.lower().map(keywords_all).fillna(df_exploded['description_tokens'])
    df_exploded = df_exploded[df_exploded['keywords'] != '']
    
    # Group by date and keywords, then count occurrences
    grouped = df_exploded.groupby(['date', 'keywords']).size().reset_index(name='counts')
    
    # Merge with daily total job counts to compute the percentage
    jobs_per_date = jobs_df.groupby('date').size().reset_index(name='total_jobs')
    grouped = grouped.merge(jobs_per_date, on='date')
    grouped['percentage'] = grouped['counts'] / grouped['total_jobs']
    
    return grouped.drop(columns=['total_jobs'])

skill_count = agg_skill_data(jobs_all)

# Top page build
st.markdown("## 🛠️ What is the TOP Skill for Data Analysts?!?")
col1, col2, col3, col4 = st.columns(4)
with col1:
    keyword_list = ["All Tools", "Languages"]
    keyword_choice = st.radio('Skill:', keyword_list, horizontal=False)
with col4:
    graph_list = ["All Time", "Daily Trend"]
    graph_choice = st.radio('Time:', graph_list, horizontal=False)

# Skill list for slicer... NOT USED
select_all = "Select All"
skills = list(skill_count.keywords)
skills.insert(0, select_all)

# Number skill selctor for slider
skill_dict = {"Top 5": 5, "Top 10": 10, "Top 20": 20, "Top 50": 50, "All 🥴" : len(skill_count)}

# Platform sort, count, and filter for slicer
platform_count = jobs_all.via.value_counts().rename_axis('platforms').reset_index(name='counts')
platform = list(platform_count.platforms)
platform.insert(0, select_all)

# Other Filter data for slicers
job_type = pd.DataFrame(jobs_all.schedule_type.drop_duplicates())
job_type = job_type[job_type.schedule_type.notna()]
job_type = list(job_type.schedule_type)
job_type.insert(0, select_all)

with st.sidebar:
    st.markdown("# 🛠️ Filters")
    top_n_choice = st.radio("Data Skills:", list(skill_dict.keys()))
    job_type_choice = st.radio("Job Type:", job_type)
    platform_choice = st.selectbox("Social Platform:", platform)

# Side column filter data transform
if platform_choice != select_all:
    jobs_all = jobs_all[jobs_all.via.apply(lambda x: platform_choice in x)]
if job_type_choice != select_all:
    jobs_all = jobs_all[jobs_all.schedule_type.apply(lambda x: job_type_choice in str(x))]

# Skill Filters - top n and languages
skill_all_time = agg_skill_data(jobs_all)
skill_filter = skill_dict[top_n_choice]
if keyword_choice != keyword_list[0]:
    skill_all_time = skill_all_time[skill_all_time.keywords.isin(list(keywords_programming.values()))]
skill_all_time = skill_all_time.head(skill_filter)
skill_all_time_list = list(skill_all_time.keywords)


# All time line chart
selector = alt.selection_single(encodings=['x', 'y'])
all_time_chart = alt.Chart(skill_all_time).mark_bar(
    cornerRadiusTopLeft=10,
    cornerRadiusTopRight=10    
).encode(
    x=alt.X('keywords', sort=None, title="", axis=alt.Axis(labelFontSize=20) ),
    y=alt.Y('percentage', title="Likelyhood to be in Job Posting", axis=alt.Axis(format='%', labelFontSize=17, titleFontSize=17)),
    color=alt.condition(selector, 'percentage', alt.value('lightgray'), legend=None),
    tooltip=["keywords", alt.Tooltip("percentage", format=".1%")]
).add_selection(
    selector
).configure_view(
    strokeWidth=0
)

skill_daily_data = agg_skill_daily_data(jobs_all)
skill_daily_data = skill_daily_data[skill_daily_data.keywords.isin(skill_all_time_list)]

# Daily trend line chart
source = skill_daily_data
x = 'date'
y = 'percentage'
color = 'keywords'
selector = alt.selection_single(encodings=['x', 'y'])
hover = alt.selection_single(
    fields=[x],
    nearest=True,
    on="mouseover",
    empty="none",
)
lines = (
    alt.Chart(source)
    .mark_line(point="transparent")
    .encode(x=alt.X(x, title="Date", axis=alt.Axis(labelFontSize=15, titleFontSize=17)), 
        y=alt.Y(y, title="Likelyhood to be in Job Posting", 
        axis=alt.Axis(format='%', labelFontSize=17, titleFontSize=17)), 
        color=color)
    .transform_calculate(color='datum.delta < 0 ? "red" : "lightblue"')
)
points = (
    lines.transform_filter(hover)
    .mark_circle(size=65)
    .encode(color=alt.Color("color:N", scale=None))
)
tooltips = (
    alt.Chart(source)
    .mark_rule(opacity=0)
    .encode(
        x=x,
        y=y,
        tooltip=[color, alt.Tooltip(y, format=".1%"), x],
    )
    .add_selection(hover)
)
daily_trend_chart = (lines + points + tooltips).interactive().configure_view(strokeWidth=0)

if graph_choice == graph_list[0]:
    st.altair_chart(all_time_chart, use_container_width=True)
else:
    st.altair_chart(daily_trend_chart, use_container_width=True)
