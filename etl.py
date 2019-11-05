import os
import glob
import psycopg2
import pandas as pd
from sql_queries import *
import numpy as np

def process_song_file(cur, filepath):
    """
    Description: This function is used to read files under filepath (data/song_data) and insert data into songs and artists tables. 

    Arguments:
        cur: a cursor object. 
        filepath: song data file path. 

    Returns:
        None
    """

    # open song file
    df = pd.read_json(filepath, lines=True)

    # insert song record
    song_data = df.loc[0, ["song_id",  "title", "artist_id", "year", "duration"]]
    song_data[3] = int(song_data.values.tolist()[3])
    cur.execute(song_table_insert, song_data)
    
    # insert artist record
    artist_data = df.loc[0, ["artist_id",  "artist_name", "artist_location", "artist_latitude", "artist_longitude"]].values
    cur.execute(artist_table_insert, artist_data)


def process_log_file(cur, filepath):
    """
    Description: This function is used to read files in filepath (data/log_data) and insert data into users, time, songplays tables. 

    Arguments:
        cur: a cursor object. 
        filepath: log data file path. 

    Returns:
        None
    """

    # open log file
    df = pd.read_json(filepath, lines=True)

    # filter by NextSong action
    df = df.loc[df['page'] == 'NextSong']

    # convert timestamp column to datetime
    t = pd.to_datetime(df.ts, unit='ms')
    
    # insert time data records
    hours = t.dt.hour.values
    days = t.dt.day.values
    weeks = t.dt.week.values
    months = t.dt.month.values
    years = t.dt.year.values
    weekdays = t.dt.weekday.values

    dic = {
           'start_time': t, 
           'hour': hours, 
           'day': days, 
           'week': weeks, 
           'month': months, 
           'year': years, 
           'weekday': weekdays
    }
    time_df = pd.DataFrame.from_dict(dic)

    for i, row in time_df.iterrows():
        cur.execute(time_table_insert, list(row))

    # load user table
    user_df = df[['userId', 'firstName', 'lastName', 'gender', 'level']]

    # insert user records
    for i, row in user_df.iterrows():
        cur.execute(user_table_insert, row)

    # insert songplay records
    for index, row in df.iterrows():
        
        # get songid and artistid from song and artist tables
        cur.execute(song_select, (row.song, row.artist, row.length))
        results = cur.fetchone()
        
        if results:
            songid, artistid = results
        else:
            songid, artistid = None, None

        # insert songplay record
        datetime_without_timezone = pd.to_datetime(row.ts, unit='ms')
        songplay_data = (datetime_without_timezone, row.userId, row.level, songid, artistid, row.sessionId, row.location, row.userAgent)
        cur.execute(songplay_table_insert, songplay_data)

        

def process_data(cur, conn, filepath, func):
    """
    Description: This function is used to get all files under filepath and execute function func to process each file. 

    Arguments:
        cur: a cursor object. 
        conn: a connection object
        filepath: a file path
        func: a function to process file

    Returns:
        None
    """

    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,'*.json'))
        for f in files :
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        print('{}/{} files processed.'.format(i, num_files))


def main():
    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=student password=student")
    conn.set_session(autocommit=True)
    cur = conn.cursor()

    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    conn.close()


if __name__ == "__main__":
    main()