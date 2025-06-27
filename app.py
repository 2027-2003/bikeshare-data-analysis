import pandas as pd
import streamlit as st
st.set_page_config(page_title="US Bikeshare", page_icon="🚴", layout="wide")
st.markdown(

    """
    <style>
    body {
        background-color: #e6f2ff; /* Sky Blue */
        color: #1a2b4c; /* Navy Blue */
    }
    .stApp {
        background-color: #e6f2ff;
    }
    .css-18ni7ap.e8zbici2 {
        background-color: #f2f2f2; /* Light Gray Sidebar */
    }
    h1, h2, h3, h4 {
        color: #009688; /* Teal Green Titles */
    }
    .css-1d391kg {  /* Text color fallback */
        color: #1a2b4c !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)
# App page configuration


# Main title formatting
st.markdown("<h1 style='text-align: center; color: #4CAF50;'>🚴‍♂ US Bikeshare Data Explorer</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color: #555;'>Use the filters below to explore bikeshare data 👇</h4>", unsafe_allow_html=True)

# Sidebar filters
st.sidebar.markdown("## 🎯 Filters")
CITY_DATA = {
    'Chicago': 'chicago.csv',
    'New York': 'new_york_city.csv',
    'Washington': 'washington.csv'
}
city = st.sidebar.selectbox("Select a city:", list(CITY_DATA.keys()))
month = st.sidebar.selectbox("Select a month:", ['all', 'January', 'February', 'March', 'April', 'May', 'June'])
day = st.sidebar.selectbox("Select a day:", ['all', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])

# Load data
@st.cache_data
def load_data(city):
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month_name()
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour
    return df

df = load_data(city)

# Apply filters
if month != 'all':
    df = df[df['month'] == month]
if day != 'all':
    df = df[df['day_of_week'] == day]

# Display filtered data
st.markdown("### 📄 First 5 Rows After Filtering:")
st.dataframe(df.head(), use_container_width=True)

# Time statistics
st.markdown("### ⏱ Time Statistics:")
st.info(f"*Most Common Month:* {df['month'].mode()[0]}")
st.info(f"*Most Common Day:* {df['day_of_week'].mode()[0]}")
st.info(f"*Most Common Start Hour:* {df['hour'].mode()[0]}")

# Station statistics
st.markdown("### 🚏 Most Popular Stations:")
st.success(f"*Most Common Start Station:* {df['Start Station'].mode()[0]}")
st.success(f"*Most Common End Station:* {df['End Station'].mode()[0]}")
df['trip'] = df['Start Station'] + " → " + df['End Station']
st.success(f"*Most Common Trip:* {df['trip'].mode()[0]}")

# Trip duration statistics
st.markdown("### ⏳ Trip Duration:")
st.warning(f"*Total Travel Time:* {df['Trip Duration'].sum()} seconds")
st.warning(f"*Average Trip Duration:* {df['Trip Duration'].mean():.2f} seconds")

# User statistics
st.markdown("### 👤 User Statistics:")
st.markdown("*User Types Count:*")
st.code(df['User Type'].value_counts().to_string())

if 'Gender' in df.columns:
    st.markdown("*Gender Count:*")
    st.code(df['Gender'].value_counts().to_string())

if 'Birth Year' in df.columns:
    st.markdown("*Birth Year Statistics:*")
    st.code(f"Earliest Year: {int(df['Birth Year'].min())}")
    st.code(f"Most Recent Year: {int(df['Birth Year'].max())}")
    st.code(f"Most Common Year: {int(df['Birth Year'].mode()[0])}")

st.success("✅ Analysis completed successfully!")

# Footer
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("<center><small style='color:gray;'>📊 Bikeshare Data Project using Streamlit | Designed by: Mishal</small></center>", unsafe_allow_html=True)
