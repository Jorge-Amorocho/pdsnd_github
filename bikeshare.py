import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

MONTHS = ['january', 'february', 'march', 'april', 'may', 'june', 'all']

def check_input(input_str, input_type):
    cities = ['chicago', 'new york city', 'washington']
    while True:
        input_read=input(input_str).lower()
        try:
            if input_read in cities and input_type==1:
                break
            elif input_read in MONTHS and input_type==2:
                break
            elif input_read in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'all'] and input_type==3:
                break
            else:
                if input_type==1:
                    print('Wrong City. Please type one of the following:', cities)
                if input_type==2:
                    print('wrong month')
                if input_type==3:
                    print('wrong day')
        except ValueError:
            print('Sorry Error Input')
    return input_read

def get_filters():
    city=check_input('chicago, new york city or washington? ', 1)
    month=check_input('month? ', 2)
    day=check_input('day? ', 3)
    print('-'*39)
    return city, month, day
    # return "chicago", "january", "monday"


def load_data(city, month, day):
    """
    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    df = pd.read_csv(CITY_DATA[city])

    df['Start Time'] = pd.to_datetime(df['Start Time'])

    df['month'] = df['Start Time'].dt.month  # int
    df['day_of_week'] = df['Start Time'].dt.weekday_name  # Friday
    df['hour'] = df['Start Time'].dt.hour  # 24h

    if month != 'all':
        # convert month from text to int
        months = MONTHS # ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        # import pdb; pdb.set_trace()
        df = df[df['month'] == month]  # collect rows for this month only

    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df

def time_stat(df):
    start_time = time.time()
    print(df['month'].mode()[0])
    print(df['day_of_week'].mode()[0])
    print(df['hour'].mode()[0])
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stat(df):
    start_time = time.time()
    print(df['Start Station'].mode()[0])
    print(df['End Station'].mode()[0])
    group_field= df.groupby(['Start Station', 'End Station'])
    print(group_field.size().sort_values(ascending=False))
    print("\nThis took %s seconds." % (time.time() - start_time))

    popular_start_station = df['Start Station'].mode()[0]

    print('Most Start Station:', popular_start_station)

    popular_end_station = df['End Station'].mode()[0]

    print('Most End Station:', popular_end_station)

    group_field= df.groupby(['Start Station', 'End Station'])
    popular_combination_station = group_field.size().sort_values(ascending=False).head(1)
    print('Most frequent combination of Start Station and End Station trip:\n', popular_combination_station)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_stat(df):
    print('\nTrip Total and Average\n') ###
    start_time = time.time()
    print(df['Trip Duration'].sum())
    print(df['Trip Duration'].mean())
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stat(df,city):
    print('\nUser Infos\n')
    start_time = time.time()
    print(df['User Type'].value_counts())
    if city!= 'washington':
        print(df['Gender'].value_counts())
        print(df['Birth Year'].mode()[0])
        print(df['Birth Year'].max())
        print(df['Birth Year'].min())
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def show_raw_data(frame, num_lines=5):
    '''
    '''
    while True:
        question = "do you want to see {} lines of raw data? yes, no? ".format(num_lines)
        answer = input(question).lower()
        if answer == 'no':
            break
        elif answer == 'yes':
            lines = frame.iloc[:num_lines]
            print(lines)
        else:
            pass

def main():
    while True:
        city, month, day = get_filters()
        df= load_data(city, month, day)
        time_stat(df)
        station_stat(df)
        trip_stat(df)
        user_stat(df,city)
        show_raw_data(df)
        restart = input('try again? yes, no ')
        if restart.lower() !='yes':
            print("goodbye")
            break

if __name__ == "__main__":
	main()
