import time
import pandas as pd
import numpy as np
import calendar


CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }


def get_filters():

    print("Hello! Let's explore some US bikeshare data!\n")

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input("Which city's data would you like to see?\nPlease enter either Chicago, New York City or Washington.\n").lower()
    while city.lower() not in ['chicago', 'new york city', 'washington']:
        print("\nWrong entry!\n")
        city = input("Which city's data would you like to see?\nPlease enter either Chicago, New York City or Washington.\n").lower()

    # get user input for month (all, january, february, ... , june)
    months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
    month = input("\nWhich month's data would you like to see?\nPlease enter either January, February, March, April, May, June or all\n").lower()
    while month not in months:
        print("\nSorry, there is no such data.\n")
        month = input("Which month's data would you like to see?\nPlease enter either January, February, March, April, May, June or all\n").lower()

    # get user input for day of week (all, monday, tuesday, ... sunday)
    days = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'all']
    day = input("\nWhich day's data would you like to see?\nPlease enter any day of the week.\n").lower()
    while day not in days:
        print("\nSorry, there is no such data.\n")
        day = input("Which day's data would you like to see?\nPlease enter any day of the week.\n").lower()


    print('-'*40)
    return city, month, day



def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.
    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    # Load data file into DataFrame
    df = pd.read_csv(CITY_DATA[city])

    # Convert the Start Time column to to_datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # Extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour

    # Filter by month if applicable
    if month != 'all':
        # Use the index of the months list to get the corresponding integer
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # Filter by month to create the new dataframe
        df = df[df['month'] == month]

    # Filter data by day of week if applicable
    if day != 'all':
        # Filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df



def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month

    common_month = df['month'].mode()[0]
    common_month = calendar.month_name[common_month]
    print('The most common month of travel is {}'.format(common_month))


    # display the most common day of week
    common_day = df['day_of_week'].mode()[0]
    print('The most common travel day of the week is {}'.format(common_day))


    # display the most common start hour
    common_hour = df['hour'].mode()[0]
    print('The most common hour of travel is {}'.format(common_hour))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start_station = df['Start Station'].mode()[0]
    print('The most commonly used start station is {}'.format(common_start_station))


    # display most commonly used end station
    common_end_station = df['End Station'].mode()[0]
    print('The most commonly used end station is {}'.format(common_end_station))


    # display most frequent combination of start station and end station trip
    common_start_end_station = df.groupby(['Start Station'])['End Station'].value_counts().index[0]

    print('The most frequent combination of Start Station and End Station is {}'.format(common_start_end_station))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)



def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()

    dys = total_travel_time // (24*3600)
    hr = total_travel_time % (24*3600) // 3600
    mins = total_travel_time % (24*3600) % 3600 // 60
    sec = total_travel_time % (24*3600) % 3600 % 60
    print('The total trip duration is {} days, {} hours, {} minutes and {} seconds'.format(dys, hr, mins, sec))

    # display mean travel time
    avg_travel_time = df['Trip Duration'].mean()

    dys = avg_travel_time // (24*3600)
    hr = avg_travel_time % (24*3600) // 3600
    mins = avg_travel_time % (24*3600) % 3600 // 60
    sec = avg_travel_time % (24*3600) % 3600 % 60
    print('The average trip duration is {} days, {} hours, {} minutes and {} seconds'.format(dys, hr, mins, sec))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('The breakdown of user types: {}'.format(user_types))


    # Display counts of gender
    if 'Gender' in df.columns:
        gender = df['Gender'].value_counts()
        print('\nThe breakdown of male and female users: {}'.format(gender))
    else:
        print('\nNo gender column present')


    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        earliest_birth_year = df['Birth Year'].min()
        print('\nThe earliest birth year is {}'.format(earliest_birth_year))
        most_recent_birth_year = df['Birth Year'].max()
        print('\nThe most recent birth year is {}'.format(most_recent_birth_year))
        most_common_birth_year = df['Birth Year'].mode()[0]
        print('\nThe most common birth year is {}'.format(most_common_birth_year))
    else:
        print('\nNo birth year column present')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_raw_data(df):
    """ Ask the user if they want to see 5 lines of raw data and displays 5 lines
    at a time """

    raw_data = input("Would you like to see 5 lines of raw data? Enter yes or no.\n")
    if raw_data.lower() == 'yes':
        start_loc = 0
        while True:
            print(df.iloc[start_loc: start_loc+5])
            start_loc += 5
            next_data = input("Would you like to see the next 5 lines? Enter yes or no.\n")
            if next_data != 'yes':
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


        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
