import time
import pandas as pd
import numpy as np

import calendar

CITY_DATA = {'chicago': 'chicago.csv',
             'new york': 'new_york_city.csv',
             'washington': 'washington.csv'}


def get_filters():
    """
    Asks the user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs

    city = ""
    while city.lower() not in ["chicago", "new york", "washington"]:
        city = input(
            "Would you like to see data for Chicago, New York, or Washington?\n")

    month = 'all'
    day = 'all'

    choice = ""
    while choice not in ["month", "day", "none", "both"]:
        choice = input(
            "Would you like to filter the data by month, day, both, or not at all? Type 'none' for no time filter\n")

    # get user input for month (all, january, february, ... , june)
    if choice in ["month", "both"]:
        months_dict = {month: index for index,
                       month in enumerate(calendar.month_name) if month}

        month_str = ""
        while month_str.lower() not in ["january", "february", "march", "april", "May", "June", "all"]:
            month_str = input(
                "Which month? January, February, March, April, May or June?\n")
        if month_str != "all":
            month = months_dict[month_str]
    # get user input for day of week (all, monday, tuesday, ... sunday)
    if choice in ["day", "both"]:
        day = ""

        while day.lower() not in ["1", "2", "3", "4", "5", "6", "7", "all"]:
            day = (input(
                "Which day? Please type response as an integer(e.g., 1=Sunday, 2=Monday ...).\n"))

    print('-'*80)
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
    df = pd.read_csv(CITY_DATA[city.lower()])

    # convert the Start Time & End Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])

    # extract month and day of week from Start Time to create new columns
    df['start_month'] = df['Start Time'].dt.month
    df['start_day_of_week'] = df['Start Time'].dt.weekday+1

    # extract month and day of week from End Time to create new columns
    df['end_month'] = df['End Time'].dt.month
    df['end_day_of_week'] = df['End Time'].dt.weekday+1

    # filter by month if applicable

    if month != 'all':
        # filter by month to create the new dataframe
        df = df[df['start_month'] == int(month)]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['start_day_of_week'] == int(day)]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel.
    Args:
        takes the working dataframe
    Prints:
        print its results to command pletter, also it can be modified to serve an api or echo to a web form
    """

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    popular_start_month = df['start_month'].mode()[0]
    popular_start_month_count = df[df['start_month'] == df['start_month'].mode()[
        0]]['start_month'].count()
    print("Most popular hour: ", popular_start_month,
          "\tCounts: ", popular_start_month_count)
    # display the most common day of week
    popular_start_day = df['start_day_of_week'].mode()[0]
    popular_start_day_count = df[df['start_day_of_week'] == df['start_day_of_week'].mode()[
        0]]['start_day_of_week'].count()
    print("Most popular day of the week: ", popular_start_day,
          "\tCounts: ", popular_start_day_count)
    # display the most common start hour
    popular_start_hour = df['Start Time'].dt.hour.mode()[0]
    popular_start_hour_count = df[df['Start Time'].dt.hour ==
                                  df['Start Time'].dt.hour.mode()[0]]['Start Time'].count()
    print("Most popular hour of the day: ", popular_start_hour,
          "\tcounts: ", popular_start_hour_count)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*80)


def station_stats(df):
    """Displays statistics on the most popular stations and trip.
    Args:
        takes the working dataframe
    Prints:
        print its results to command pletter, also it can be modified to serve an api or echo to a web form
    """

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df["Start Station"].value_counts().idxmax()
    popular_start_station_count = df["Start Station"].value_counts().max()
    print("the most commonly used start station is '",
          popular_start_station, "'\tCounts: ", popular_start_station_count)
    # display most commonly used end station
    popular_end_station = df["End Station"].value_counts().idxmax()
    popular_end_station_count = df["End Station"].value_counts().max()
    print("the most commonly used End station is '",
          popular_end_station, "'\tCounts: ", popular_end_station_count)
    # display most frequent combination of start station and end station trip
    popular_startend_station = df[[
        "Start Station", "End Station"]].value_counts().idxmax()
    popular_startend_station_count = df[[
        "Start Station", "End Station"]].value_counts().max()
    print("the most frequent combination of start station and end station trip is '",
          popular_startend_station, "'\tCounts: ", popular_startend_station_count)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*80)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration.
    Args:
        takes the working data frame
    Prints:
        print its results to command pletter, also it can be modified to serve an api or echo to a web form
    """

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    df["duration"] = (df["End Time"] - df["Start Time"]).dt.seconds
    # display total travel time
    total_travel_secs = df["duration"].sum()

    days, hours, minutes, seconds = date_time_destructor(total_travel_secs)

    print("total travel time:", total_travel_secs, " which means ", days, " days ", hours,
          " hours ", minutes, " minutes ", seconds, "seconds")

    # display mean travel time
    total_travel_mean_secs = df["duration"].mean()
    days, hours, minutes, seconds = date_time_destructor(
        total_travel_mean_secs)

    print("total Avg Duration time: ", total_travel_mean_secs, " which is ", days, " days ", hours,
          " hours ", minutes, " minutes ", seconds, "seconds")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*80)


def user_stats(df):
    """Displays statistics on bikeshare users.
    Args:
        takes the working dataframe
    Prints:
        print its results to command pletter, also it can be modified to serve an api or echo to a web form
    """

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print(df.groupby(["User Type"])["User Type"].count())

    # Display counts of gender only for chicago and new york
    if "Gender" in df.columns:
        print(df.groupby(["Gender"])["Gender"].count())

    # Display earliest, most recent, and most common year of birth only for chicago and new york
    if "Birth Year" in df.columns:
        print("the Earliest year of birth is ", df["Birth Year"].min(), " which have an Avg. travel duration of ", (
            df[df["Birth Year"] == df["Birth Year"].min()])["Trip Duration"].mean(), "for this age")
        print("the most recent year of birth is ", df["Birth Year"].max(), " which have an Avg. travel duration of ", (
            df[df["Birth Year"] == df["Birth Year"].max()])["Trip Duration"].mean(), " for this age")
        print("the most common year of birth is ",
              df["Birth Year"].value_counts().idxmax(), " which have an Avg. travel duration of ", (df[df["Birth Year"] == df["Birth Year"].value_counts().idxmax()])["Trip Duration"].mean(), " for this age")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*80)


def date_time_destructor(time_in_secs):
    """function to convert num.of seconds into days, hours, mins, secs
    Args:
        number of seconds we have
    Returns:
        a tuple of days, hours, minutes, seconds that had been calculatwed
    """
    seconds_in_day = 60 * 60 * 24
    seconds_in_hour = 60 * 60
    seconds_in_minute = 60

    days = time_in_secs // seconds_in_day
    hours = (time_in_secs - (days * seconds_in_day)) // seconds_in_hour
    minutes = (time_in_secs - (days * seconds_in_day) -
               (hours * seconds_in_hour)) // seconds_in_minute
    seconds = (time_in_secs - (days * seconds_in_day) -
               (hours * seconds_in_hour) - (minutes * seconds_in_minute))

    return (days, hours, minutes, seconds)


def individual_stat(df):
    indvidual_trip_inc = 0

    df.rename({"Unnamed: 0": ""}, axis=1, inplace=True)
    df.reset_index(drop=True, inplace=True)

    indvidual_trip_str = ""
    while indvidual_trip_str.lower() not in ["yes", "no"]:
        indvidual_trip_str = input(
            '\nWould you like to view individual trip data?Type "yes" or "no".\n')
        if indvidual_trip_str.lower() == 'no':
            indvidual_trip_str = ""
            break

        dummy_flag = 0
        if "Gender" not in df.columns:
            dummy_flag = 1
        if "Birth Year" not in df.columns:
            dummy_flag = 1

        if dummy_flag:
            print(df[['',
                  'End Station',
                      'End Time',
                      'Start Station',
                      'Start Time',
                      'Trip Duration',
                      'User Type']].loc[indvidual_trip_inc:indvidual_trip_inc+1].to_dict('records')[0])
        else:
            print(df[['',
                  'Birth Year',
                      'End Station',
                      'End Time',
                      'Gender',
                      'Start Station',
                      'Start Time',
                      'Trip Duration',
                      'User Type']].loc[indvidual_trip_inc:indvidual_trip_inc+1].to_dict('records')[0])

        indvidual_trip_inc += 1

        if indvidual_trip_str.lower() == 'yes':
            indvidual_trip_str = ""
            continue


def main():
    """main loop for running or application"""
    while True:
        city, month, day = get_filters()
        print("our Filter parameters city: ", city,
              "\tMonth: ", month, "\tday: ", day)
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        individual_stat(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() == 'no':
            break
        # by default it would restart and if yes restart


if __name__ == "__main__":
    main()


# [{"Unnamed: 0":1423854,"Start Time":1498230572000,"End Time":1498230893000,"Trip Duration":321,"Start Station":"Wood St & Hubbard St","End Station":"Damen Ave & Chicago Ave","User Type":"Subscriber","Gender":"Male","Birth Year":1992.0,"start_month":6,"start_day_of_week":5,"end_month":6,"end_day_of_week":5,"duration":321},
# {"Unnamed: 0":955915,"Start Time":1495736343000,"End Time":1495737953000,"Trip Duration":1610,"Start Station":"Theater on the Lake","End Station":"Sheffield Ave & Waveland Ave","User Type":"Subscriber","Gender":"Female","Birth Year":1992.0,"start_month":5,"start_day_of_week":4,"end_month":5,"end_day_of_week":4,"duration":1610},
# {"Unnamed: 0":9031,"Start Time":1483518469000,"End Time":1483518885000,"Trip Duration":416,"Start Station":"May St & Taylor St","End Station":"Wood St & Taylor St","User Type":"Subscriber","Gender":"Male","Birth Year":1981.0,"start_month":1,"start_day_of_week":3,"end_month":1,"end_day_of_week":3,"duration":416}]
