import pandas as pd
from tabulate import tabulate

CITY_DATA = {
    'chicago': 'chicago.csv',
    'new york': 'new_york_city.csv',
    'washington': 'washington.csv'
}

def get_filters():
    print('\nمرحبًا بك في مشروع تحليل بيانات الدراجة! 🚴')
    while True:
        city = input('اختر مدينة (chicago / new york / washington): ').lower()
        if city in CITY_DATA:
            break
        print('❌ اسم المدينة غير صحيح.')

    months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
    while True:
        month = input('اختر شهر (january - june) أو all: ').lower()
        if month in months:
            break
        print('❌ اسم الشهر غير صحيح.')

    days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']
    while True:
        day = input('اختر يوم من الأسبوع أو all: ').lower()
        if day in days:
            break
        print('❌ اسم اليوم غير صحيح.')

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
    print('\n📊 إحصائيات الوقت:')
    print(tabulate([
        ['أكثر الشهور استخدامًا', df['month'].mode()[0].title()],
        ['أكثر الأيام استخدامًا', df['day_of_week'].mode()[0].title()],
        ['أكثر الساعات استخدامًا', df['hour'].mode()[0]]
    ], headers=['البند', 'القيمة'], tablefmt='grid'))

def station_stats(df):
    print('\n📍 إحصائيات المحطات:')
    common_trip = df['Start Station'] + " → " + df['End Station']
    print(tabulate([
        ['أكثر محطة انطلاق', df['Start Station'].mode()[0]],
        ['أكثر محطة وصول', df['End Station'].mode()[0]],
        ['أشهر رحلة', common_trip.mode()[0]]
    ], headers=['البند', 'القيمة'], tablefmt='grid'))

def trip_duration_stats(df):
    print('\n⏱ إحصائيات مدة الرحلة:')
    print(tabulate([
        ['المدة الإجمالية (ثواني)', df['Trip Duration'].sum()],
        ['متوسط المدة (ثواني)', round(df['Trip Duration'].mean(), 2)]
    ], headers=['البند', 'القيمة'], tablefmt='grid'))

def user_stats(df):
    print('\n🧑‍💼 إحصائيات المستخدمين:')
    rows = []

    # نوع المستخدم
    user_types = df['User Type'].value_counts()
    for user_type, count in user_types.items():
        rows.append([f'عدد {user_type}', count])

    # الجنس
    if 'Gender' in df.columns:
        gender_counts = df['Gender'].value_counts()
        for gender, count in gender_counts.items():
            rows.append([f'عدد {gender}', count])
    else:
        rows.append(['الجنس', 'غير متوفر'])

    # سنة الميلاد
    if 'Birth Year' in df.columns:
        rows.append(['أقدم سنة ميلاد', int(df['Birth Year'].min())])
        rows.append(['أحدث سنة ميلاد', int(df['Birth Year'].max())])
        rows.append(['أكثر سنة ميلاد شيوعًا', int(df['Birth Year'].mode()[0])])
    else:
        rows.append(['سنة الميلاد', 'غير متوفرة'])

    print(tabulate(rows, headers=['البند', 'القيمة'], tablefmt='grid'))

def display_raw_data(df):
    i = 0
    while True:
        raw = input('\nهل تريد عرض 5 صفوف من البيانات الخام؟ (yes/no): ').lower()
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

        restart = input('\nهل تريد إعادة التشغيل؟ (yes/no): ').lower()
        if restart != 'yes':
            print('شكراً لك 🌟')
            break
            # واجهة التطبيق
            st.title("🚴‍♀ US Bikeshare Data Explorer")
            st.markdown("تحليل بيانات الدراجات في الولايات المتحدة بطريقة تفاعلية.")

            # اختيارات المستخدم
            city = st.selectbox("اختر مدينة:", list(CITY_DATA.keys()))
            month = st.selectbox("اختر شهر:", ['All', 'January', 'February', 'March', 'April', 'May', 'June'])
            day = st.selectbox("اختر يوم من الأسبوع:",
                               ['All', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])

            # تحميل وتصفية البيانات
            df = load_data(city)
            if month != 'All':
                df = df[df['month'] == month.lower()]
            if day != 'All':
                df = df[df['day_of_week'] == day.lower()]

            # إحصائيات الأوقات
            st.header("📅 إحصائيات الوقت")
            st.write(f"*الشهر الأكثر شيوعًا:* {df['month'].mode()[0].title()}")
            st.write(f"*اليوم الأكثر شيوعًا:* {df['day_of_week'].mode()[0].title()}")
            st.write(f"*الساعة الأكثر شيوعًا:* {df['hour'].mode()[0]}")

            # رسم بياني للساعة
            st.subheader("⏰ توزيع الرحلات حسب الساعة")
            fig, ax = plt.subplots()
            df['hour'].value_counts().sort_index().plot(kind='bar', ax=ax)
            ax.set_xlabel("الساعة")
            ax.set_ylabel("عدد الرحلات")
            st.pyplot(fig)

            # إحصائيات المحطات
            st.header("🚏 إحصائيات المحطات")
            st.write(f"*أكثر محطة بداية:* {df['Start Station'].mode()[0]}")
            st.write(f"*أكثر محطة نهاية:* {df['End Station'].mode()[0]}")
            df['Trip'] = df['Start Station'] + " → " + df['End Station']
            st.write(f"*الرحلة الأكثر شيوعًا:* {df['Trip'].mode()[0]}")

            # إحصائيات مدة الرحلة
            st.header("⏳ مدة الرحلة")
            st.write(f"*المدة الإجمالية (ثانية):* {df['Trip Duration'].sum():,.0f}")
            st.write(f"*متوسط المدة (ثانية):* {df['Trip Duration'].mean():.2f}")

            # إحصائيات المستخدم
            st.header("👤 إحصائيات المستخدم")
            st.write("*أنواع المستخدمين:*")
            st.dataframe(df['User Type'].value_counts())

            if 'Gender' in df.columns:
                st.write("*الجنس:*")
                st.dataframe(df['Gender'].value_counts())
            else:
                st.warning("🚫 بيانات الجنس غير متوفرة في هذا الملف.")

            if 'Birth Year' in df.columns:
                st.write(f"*أقدم سنة ميلاد:* {int(df['Birth Year'].min())}")
                st.write(f"*أحدث سنة ميلاد:* {int(df['Birth Year'].max())}")
                st.write(f"*أكثر سنة ميلاد شيوعًا:* {int(df['Birth Year'].mode()[0])}")
            else:
                st.warning("🚫 بيانات سنة الميلاد غير متوفرة في هذا الملف.")

            # عرض البيانات الخام
            if st.checkbox("📄 عرض أول 5 صفوف من البيانات الخام"):
                st.dataframe(df.head())

if __name__ == "__main__":
    main()