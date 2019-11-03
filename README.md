# data-modeling-with-postgres
A startup called Sparkify wants to analyze the data they've been collecting on songs and user activity on their new music streaming app. This project is to create a Postgres database and build an ETL pipeline to transfer data from song and log directories into tables using Python and SQL.


### Table of Contents
* [Data](#Data)
* [Tables](#Tables)
* [Steps to run scripts](#Steps)


### Data
* Song Dataset: 
    - Each JSON file nested in subdirectories under /data/song_data contains metadata about a song and the artist of that song. 
    - The files are partitioned by the first three letters of each song's track ID. For example, you can find a song with track ID `ABCEI128F424C983` in `/data/song_data/A/B/C` folder.
    - Here is what a single song file, TRAABJL12903CDCF1A.json, looks like.
    ```
    {
        "num_songs": 1, 
        "artist_id": "ARJIE2Y1187B994AB7", 
        "artist_latitude": null, 
        "artist_longitude": null, 
        "artist_location": "", 
        "artist_name": "Line Renaud", 
        "song_id": "SOUPIRU12A6D4FA1E1", 
        "title": "Der Kleine Dompfaff", 
        "duration": 152.92036, 
        "year": 0
    }
    ```
* Log Dataset:
    - There are JSON files nested in subdirectories under /data/log_data. 
    - The files are partitioned by year and month. 
    - Here is what a single row in a log file, log_data/2018/11/2018-11-01-events.json, looks like.
    ```
    {
        "artist":"Survivor",
        "auth":"Logged In",
        "firstName":"Jayden",
        "gender":"M",
        "itemInSession":0,
        "lastName":"Fox",
        "length":245.36771,
        "level":"free",
        "location":"New Orleans-Metairie, LA",
        "method":"PUT",
        "page":"NextSong",
        "registration":1541033612796.0,
        "sessionId":100,
        "song":"Eye Of The Tiger",
        "status":200,
        "ts":1541110994796,
        "userAgent":"\"Mozilla\/5.0 (Windows NT 6.3; WOW64) AppleWebKit\/537.36 (KHTML, like Gecko) Chrome\/36.0.1985.143 Safari\/537.36\"",
        "userId":"101"
    }
    ```

### Tables
* There are four dimension tables and one fact tables.
    - Fact Table \
        songplays - records in log data associated with song plays i.e. records with page NextSong songplay_id, start_time, user_id, level, song_id, artist_id, session_id, location, user_agent

    - Dimension Tables \
        users - users in the app
        user_id, first_name, last_name, gender, level

        songs - songs in music database
        song_id, title, artist_id, year, duration

        artists - artists in music database
        artist_id, name, location, latitude, longitude

        time - timestamps of records in songplays broken down into specific units
        start_time, hour, day, week, month, year, weekday
* CREATE statements in `sql_queries.py` specify all columns for each of the five tables with data types and conditions.


### Steps 
* run `create_tables.py` to create database and tables.
* run `etl.py` to process the entire datasets and insert data into each table




