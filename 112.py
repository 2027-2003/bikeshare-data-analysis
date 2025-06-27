import pandas as pd
from tabulate import tabulate

CITY_DATA = {
    'chicago': 'chicago.csv',
    'new york': 'new_york_city.csv',
    'washington': 'washington.csv'
}

def get_filters():
    print('\nWelcome to the Bike Data Analysis Project! 🚴')
    while True:
        city = input('Choose a city (chicago / new york / washington): ').lower()
        if city in CITY_DATA:
            break
        print('❌ Invalid city name.')

    months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
    while True:
        month = input('Choose a month (january - june) or all: ').lower()
        if month in months:
            break
        print('❌ Invalid month name.')

    days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']
    while True:
        day = input('Choose a day of the week or all: ').lower()
        if day in days:
            break
        print('❌ Invalid day name.')

    return city, month, day

def load_data(city, month, day):
    df = pd.read_csv(CITY_DATA[city])

    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month_name().str.lower()
    df['day_of_week'] = df['Start Time'].dt.day_name().str.lower()
    df['hour'] = df['Start Time'].dt.hour

    if month != 'all':
        df = df[df['month'] == month]
    if day != 'all':
        df = df[df['day_of_week'] == day]

    return df

def time_stats(df):
    print('\n📊 Time Statistics:')
    print(tabulate([
        ['Most common month', df['month'].mode()[0].title()],
        ['Most common day', df['day_of_week'].mode()[0].title()],
        ['Most common hour', df['hour'].mode()[0]]
    ], headers=['Item', 'Value'], tablefmt='grid'))

def station_stats(df):
    print('\n📍 Station Statistics:')
    common_trip = df['Start Station'] + " → " + df['End Station']
    print(tabulate([
        ['Most common start station', df['Start Station'].mode()[0]],
        ['Most common end station', df['End Station'].mode()[0]],
        ['Most common trip', common_trip.mode()[0]]
    ], headers=['Item', 'Value'], tablefmt='grid'))

def trip_duration_stats(df):
    print('\n⏱ Trip Duration Statistics:')
    print(tabulate([
        ['Total duration (seconds)', df['Trip Duration'].sum()],
        ['Average duration (seconds)', round(df['Trip Duration'].mean(), 2)]
    ], headers=['Item', 'Value'], tablefmt='grid'))

def user_stats(df):
    print('\n🧑‍💼 User Statistics:')
    rows = []

    # User Type
    user_types = df['User Type'].value_counts()
    for user_type, count in user_types.items():
        rows.append([f'Number of {user_type}', count])

    # Gender
    if 'Gender' in df.columns:
        gender_counts = df['Gender'].value_counts()
        for gender, count in gender_counts.items():
            rows.append([f'Number of {gender}', count])
    else:
        rows.append(['Gender', 'Not available'])

    # Birth Year
    if 'Birth Year' in df.columns:
        rows.append(['Earliest birth year', int(df['Birth Year'].min())])
        rows.append(['Most recent birth year', int(df['Birth Year'].max())])
        rows.append(['Most common birth year', int(df['Birth Year'].mode()[0])])
    else:
        rows.append(['Birth year', 'Not available'])

    print(tabulate(rows, headers=['Item', 'Value'], tablefmt='grid'))

def display_raw_data(df):
    i = 0
    while True:
        raw = input('\nWould you like to view 5 rows of raw data? (yes/no): ').lower()
        if raw == 'yes':
            print(df.iloc[i:i+5])
            i += 5
        else:
            break

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_raw_data(df)

        restart = input('\nWould you like to restart? (yes/no): ').lower()
        if restart != 'yes':
            print('Thank you 🌟')
            break
            # App Interface
            st.title("🚴‍♀ US Bikeshare Data Explorer")
            st.markdown("Analyze bikeshare data in the US interactively.")

            # User selections
            city = st.selectbox("Choose a city:", list(CITY_DATA.keys()))
            month = st.selectbox("Choose a month:", ['All', 'January', 'February', 'March', 'April', 'May', 'June'])
            day = st.selectbox("Choose a day of the week:",
                               ['All', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])

            # Load and filter data
            df = load_data(city)
            if month != 'All':
                df = df[df['month'] == month.lower()]
            if day != 'All':
                df = df[df['day_of_week'] == day.lower()]

            # Time stats
            st.header("📅 Time Statistics")
            st.write(f"Most common month: {df['month'].mode()[0].title()}")
            st.write(f"Most common day: {df['day_of_week'].mode()[0].title()}")
            st.write(f"Most common hour: {df['hour'].mode()[0]}")

            # Hour distribution plot
            st.subheader("⏰ Trip count by hour")
            fig, ax = plt.subplots()
            df['hour'].value_counts().sort_index().plot(kind='bar', ax=ax)
            ax.set_xlabel("Hour")
            ax.set_ylabel("Number of trips")
            st.pyplot(fig)

            # Station stats
            st.header("🚏 Station Statistics")
            st.write(f"Most common start station: {df['Start Station'].mode()[0]}")
            st.write(f"Most common end station: {df['End Station'].mode()[0]}")
            df['Trip'] = df['Start Station'] + " → " + df['End Station']
            st.write(f"Most common trip: {df['Trip'].mode()[0]}")

            # Trip duration stats
            st.header("⏳ Trip Duration")
            st.write(f"Total duration (seconds): {df['Trip Duration'].sum():,.0f}")
            st.write(f"Average duration (seconds): {df['Trip Duration'].mean():.2f}")

            # User stats
            st.header("👤 User Statistics")
            st.write("User Types:")
            st.dataframe(df['User Type'].value_counts())

            if 'Gender' in df.columns:
                st.write("Gender:")
                st.dataframe(df['Gender'].value_counts())
            else:
                st.warning("🚫 Gender data is not available in this file.")

            if 'Birth Year' in df.columns:
                st.write(f"Earliest birth year: {int(df['Birth Year'].min())}")
                st.write(f"Most recent birth year: {int(df['Birth Year'].max())}")
                st.write(f"Most common birth year: {int(df['Birth Year'].mode()[0])}")
            else:
                st.warning("🚫 Birth year data is not available in this file.")

            # Show raw data
            if st.checkbox("📄 Show first 5 rows of raw data"):
                st.dataframe(df.head())

if __name__ == "_main_":
    main()
