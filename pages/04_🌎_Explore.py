import streamlit as st
import pandas as pd
import datetime
from pandas.api.types import (
    is_datetime64_any_dtype,
    is_numeric_dtype,
    is_object_dtype,
)
from modules.formater import Title, Footer
from modules.importer import DataImport

# Title page and footer
title = "🌎 Explore"
Title().page_config(title)
Footer().footer()

# Import data
jobs_all = DataImport().fetch_and_clean_data()

st.markdown("## 🌎 Explore the dataset")

def filter_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Adds a UI on top of a dataframe to let viewers filter columns

    Args:
        df (pd.DataFrame): Original dataframe

    Returns:
        pd.DataFrame: Filtered dataframe
    
    Source:
        https://blog.streamlit.io/auto-generate-a-dataframe-filtering-ui-in-streamlit-with-filter_dataframe/
    """
    modify = st.checkbox("Add filters", value=True)

    if not modify:
        return df

    df = df.copy()

    # Try to convert datetimes into a standard format (datetime, no timezone)
    for col in df.columns:
        if is_object_dtype(df[col]):
            try:
                df[col] = pd.to_datetime(df[col])
            except Exception:
                pass

        if is_datetime64_any_dtype(df[col]):
            df[col] = df[col].dt.tz_localize(None)

    modification_container = st.container()

    with modification_container:
        to_filter_columns = st.multiselect("Filter dataframe on", df.columns)
        for column in to_filter_columns:
            left, right = st.columns((1, 20))
            # Treat columns with < 10 unique values as categorical
            if isinstance(df[column].dtype, pd.CategoricalDtype) or df[column].nunique() < 10:
                user_cat_input = right.multiselect(
                    f"Values for {column}",
                    df[column].unique(),
                    default=list(df[column].unique()),
                )
                df = df[df[column].isin(user_cat_input)]
            elif is_numeric_dtype(df[column]):
                _min = float(df[column].min())
                _max = float(df[column].max())
                step = (_max - _min) / 100
                user_num_input = right.slider(
                    f"Values for {column}",
                    min_value=_min,
                    max_value=_max,
                    value=(_min, _max),
                    step=step,
                )
                df = df[df[column].between(*user_num_input)]
            elif is_datetime64_any_dtype(df[column]):
                user_date_input = right.date_input(
                    f"Values for {column}",
                    value=(
                        df[column].min(),
                        df[column].max(),
                    ),
                )
                if len(user_date_input) == 2:
                    user_date_input = tuple(map(pd.to_datetime, user_date_input))
                    start_date, end_date = user_date_input
                    df = df.loc[df[column].between(start_date, end_date)]
            else:
                user_text_input = right.text_input(
                    f"Substring or regex in {column}",
                )
                if user_text_input:
                    df = df[df[column].astype(str).str.contains(user_text_input)]

    return df

filtered_df = filter_dataframe(jobs_all)
row_count = len(filtered_df)

st.markdown("---")
st.markdown("### 📊 Display Settings")
col1, col2 = st.columns((1, 2))
with col1:
    max_display_rows = st.number_input(
        "Max rows to render:",
        min_value=10,
        max_value=max(10, row_count),
        value=min(1000, row_count),
        step=100,
        help="Adjust this parameter to control the maximum number of rows rendered in the table."
    )

if row_count > max_display_rows:
    st.warning(
        f"⚠️ **Showing the first {max_display_rows:,} rows out of {row_count:,} matching rows.** "
        f"Increase 'Max rows to render' above if you want to view more, or add filters to narrow down the results."
    )
    st.dataframe(filtered_df.head(max_display_rows))
else:
    st.success(f"✅ **Showing all {row_count:,} matching rows.**")
    st.dataframe(filtered_df)