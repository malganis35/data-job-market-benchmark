import pandas as pd
import streamlit as st
import kagglehub

class DataImport:
    """"
    Import data from CSV file on Google Cloud
    """
    def __init__(self):
        pass

    @st.cache_data(ttl=60*60) # ttl of one hour to keep memory in cache
    def fetch_and_clean_data(_self):
        # Download the dataset files via kagglehub
        path = kagglehub.dataset_download("lukebarousse/data-analyst-job-postings-google-search")
        csv_file_path = f"{path}/gsearch_jobs.csv"
        
        # Load only the columns actually used in the application to optimize RAM & WebSocket footprint
        cols_to_use = [
            'title', 'company_name', 'location', 'via', 'schedule_type', 
            'work_from_home', 'salary', 'date_time', 'salary_pay', 'salary_rate', 
            'salary_avg', 'salary_min', 'salary_max', 'salary_hourly', 
            'salary_yearly', 'salary_standardized', 'description_tokens', 
            'job_id', 'search_term', 'search_location'
        ]
        
        jobs_data = pd.read_csv(csv_file_path, usecols=cols_to_use).replace("'","", regex=True)
        jobs_data.date_time = pd.to_datetime(jobs_data.date_time)
        
        # Fix formatting of description tokens
        jobs_data.description_tokens = jobs_data.description_tokens.fillna("[]")
        jobs_data.description_tokens = jobs_data.description_tokens.astype(str).str.strip("[]").str.split(",")
        jobs_data.description_tokens = jobs_data.description_tokens.apply(lambda row: [x.strip(" ") for x in row])
        
        return jobs_data