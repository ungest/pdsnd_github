#!/usr/bin/env python
# coding: utf-8

# In[4]:


# %load project_2.py
import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    options = ['chicago', 'new york city', 'washington']
    while True:
        city = input('Which of these cities would you like to look into? (chicago, new york city, washington): ').lower()
        try:
            options.index(city)
            break
        except ValueError:
            print('Invalid input!\nPlease enter a city that corresponds to the available options.') 
        except KeyboardInterrupt:
            print('No State selected')
            break
    print('\n')


    # get user input for month (all, january, february, ... , june)
    months = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
    while True:
        month = input('Do you want statistics from a specific month or all(all, january, february, march, april, may, june)? Make your choice: ').lower()
        try:
            months.index(month)
            break
        except ValueError:
            print('Wrong entry!\nProvide a valid input.')
        except KeyboardInterrupt:
            print('No input provided')
            break
    if month != 'all':
        month = months.index(month) 
    print('\n')

    # get user input for day of week (all, monday, tuesday, ... sunday)
    days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']
    while True:
        day = input('Do you want statistics from a specific day of the week or all(all, monday, tuesday, wednesday, thursday, friday, saturday, sunday)? Make your choice: ').lower()
        try:
            days.index(day)
            break
        except ValueError:
            print('Wrong input\nEnter a day that corresponds to one of the provided option.')
        except KeyboardInterrupt:
            print('No input provided')
            break
    if day != 'all':
        day = days.index(day)
    print('\n')


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
    # Read the csv of the choosen city to a DataFrame
    df = pd.read_csv(CITY_DATA[city])
    
    # Change the datatypes of both 'Start Time' and 'End Time' columns to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])
    
    # Extract travel month from the 'Start Time' column and create a 'month' column
    df['month'] = df['Start Time'].dt.month
    
    # Extract day of the week from the 'Start Time' column and create a 'day' column
    df['day_of_the_week'] = df['Start Time'].dt.weekday
    
    if month != 'all':
        df = df[df['month'] == month]
        
    if day != 'all':
        df = df[df['day_of_the_week'] == day]  

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month 'mc_month'
    mc_month = df.month.mode()[0]
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    mc_month = months[mc_month - 1].title()
    print('{} is the most common month of travel from your selected data'.format(mc_month))


    # display the most common day of week 'mc_dow'
    mc_dow = df.day_of_the_week.mode()[0]
    days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    mc_dow = days[mc_dow].title()
    print('Most travels were done on {}'.format(mc_dow))


    # display the most common start hour 'mc_hour'
    mc_hour = df['Start Time'].dt.hour.mode()[0]
    print('The hour that most people began their trip was {}:00'.format(mc_hour))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station 'mc_ss'
    mc_ss = df['Start Station'].mode()[0]
    print('{} was the most commonly used Start station'.format(mc_ss))


    # display most commonly used end station 'mc_end'
    mc_end = df['End Station'].mode()[0]    
    print('{} was the most commonly used End station'.format(mc_end))


    # display most frequent combination of start station and end station trip 'mc_trip'
    df['Full trip'] ='From' +' '+ df['Start Station'] +' '+'to'+' '+df['End Station']
    mc_trip = df['Full trip'].mode()[0]
    print('Most customer\'s trip was {}'.format(mc_trip))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_duration = df['Trip Duration'].sum()
    print('The total travel time was : {} seconds'.format(total_duration))


    # display mean travel time
    avg_duration = df['Trip Duration'].mean()
    print('The average time each customer spent on a trip was {} seconds'.format(avg_duration))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = list(df['User Type'].unique())
    for user_type in user_types:
        temp_data = df[df['User Type'] == user_type]
        type_count = temp_data['User Type'].count()
        if type_count > 0:
            print('{}(s): {}'.format(user_type, type_count))
    

    # Display counts of gender
    genders = ['Male', 'Female']
    for gender in genders:
        try:
            temp_data = df[df.Gender == gender]
        except AttributeError:
            break
        else:
            gender_count = temp_data.Gender.count()
            print('{}(s): {}'.format(gender, gender_count))

    # Display earliest, most recent, and most common year of birth
    try:
        birth_year_column = df['Birth Year']
    except:
        None
    else:
        earliest = int(df['Birth Year'].min())
        print('Earliest Birth Year: {}'.format(earliest))

        most_recent = int(df['Birth Year'].max())
        print('Most recent Birth Year: {}'.format(most_recent))

        most_common = int(df['Birth Year'].mode()[0])
        print('Most common Birth Year: {}'.format(most_common))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        try:
            city, month, day = get_filters()
            df = load_data(city, month, day)

            time_stats(df)
            station_stats(df)
            trip_duration_stats(df)
            user_stats(df)
            
            # Ask user if they want to see raw data
            n = 0
            while True:
                raw_data = input('Would you like to see 5 lines of the raw data? Enter yes or no.\n')
                if raw_data == 'yes':
                    print(df[n:(n+5)])
                    n += 5
                else:
                    break

            restart = input('\nWould you like to restart? Enter yes or no.\n').lower()
            if restart.lower() != 'yes':
                break
        except KeyboardInterrupt:
            break

if __name__ == "__main__":
    main()



# In[2]:


CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

data = pd.read_csv(CITY_DATA['chicago'])
data[5:10]


# In[ ]:




