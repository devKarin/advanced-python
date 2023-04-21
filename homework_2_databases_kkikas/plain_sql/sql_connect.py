"""
This module creates sql database DINERS.

The database DINERS has two related tables CANTEEN and PROVIDER.
Available functions:
def open_connection() ->None:
    -> Creates database connection.
def create_canteen() -> None:
    -> Creates database table named CANTEEN which contains
    information about canteens in TalTech's buildings.
def create_provider() -> None:
    -> Creates database table named PROVIDER which contains
    information about canteen providers in TalTech's buildings.

"""

import sqlite3


def open_connection(database: str) -> None:
    """
    Create database connection.
    """
    global CONNECTION
    CONNECTION = sqlite3.connect(database)
    print("Database opened successfully")


def create_provider() -> None:
    """
    Create database table named PROVIDER.
    """
    CONNECTION.execute("""CREATE TABLE IF NOT EXISTS PROVIDER
        (ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        PROVIDERNAME TEXT UNIQUE NOT NULL);""")
    print("Table PROVIDER successfully created.")


def create_canteen() -> None:
    """
    Create database table named CANTEEN.
    """
    CONNECTION.execute("""CREATE TABLE IF NOT EXISTS CANTEEN
        (ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        PROVIDERID INT NOT NULL,
        NAME TEXT NOT NULL,
        LOCATION TEXT,
        TIME_OPEN INT,
        TIME_CLOSED INT,
        FOREIGN KEY (PROVIDERID) REFERENCES PROVIDER (ID)
        ON UPDATE CASCADE
        ON DELETE SET NULL);""")
    print("Table CANTEEN successfully created.")


def create_it_college_record():
    """
    Create records in CANTEEN and PROVIDER tables
    according to the canteen located in IT-College.
    """
    CONNECTION.execute("""PRAGMA foreign_keys = ON;""")
    CONNECTION.execute("""INSERT INTO PROVIDER\
                       (PROVIDERNAME)\
                       VALUES\
                       ('Bitt OÜ')""")
    CONNECTION.execute("""INSERT INTO CANTEEN\
                       (PROVIDERID, NAME, LOCATION,\
                       TIME_OPEN, TIME_CLOSED)\
                       VALUES\
                       ((SELECT ID FROM PROVIDER WHERE PROVIDERNAME='Bitt OÜ'),\
                        'bitStop KOHVIK', 'IT College, Raja 4c',\
                       930, 1600)""")
    CONNECTION.commit()
    print("IT College record created.")


def create_records_in_bulk():
    """
    Create records in CANTEEN and PROVIDER tables
    for canteens other than the one located in IT-College.
    """

    canteens = [
        ['Rahva Toit',
         "Economics- and social science building canteen",
         "Akadeemia tee 3, SOC- building",
         830,
         1830],
        ['Rahva Toit',
         "Library canteen",
         "Akadeemia tee 1/Ehitajate tee 7",
         830,
         1900
         ],
        ['Baltic Restaurants Estonia AS',
         "Main building Deli cafe",
         "Ehitajate tee 5, U01 building",
         900,
         1630
         ],
        ['Baltic Restaurants Estonia AS',
         "Main building Daily lunch restaurant",
         "Ehitajate tee 5, U01 building",
         900,
         1630
         ],
        ['Rahva toit',
         "U06 building canteen",
         "NULL",
         900,
         1600
         ],
        ['Baltic Restaurants Estonia AS',
         "Natural Science building canteen",
         "Akadeemia tee 15, SCI building",
         900,
         1600
         ],
        ['Baltic Restaurants Estonia AS',
         "ICT building canteen",
         "Raja 15/Mäepealse 1",
         900,
         1600
         ],
        ['TTÜ Sport OÜ',
         "Sports building canteen",
         "Männiliiva 7, S01 building",
         1100,
         2000
         ]
    ]

    unique_providers = {}
    providers = [provider[0]
                 for provider in canteens]

    for name in providers:
        if name.casefold() not in unique_providers:
            unique_providers[name.casefold()] = name
        else:
            continue

    providers = tuple({"name": provider}
                      for provider in unique_providers.values())

    cursor = CONNECTION.cursor()
    cursor.executemany(
        """INSERT OR REPLACE INTO PROVIDER (PROVIDERNAME) VALUES(:name);""", providers)

    for index in range(len(canteens)):
        provider_name = (canteens[index][0],)
        result = cursor.execute(
            "SELECT ID FROM PROVIDER WHERE PROVIDERNAME=? COLLATE NOCASE;", provider_name)
        res = [row[0] for row in result][0]
        canteens[index][0] = res

    CONNECTION.executemany(
        """INSERT INTO CANTEEN (PROVIDERID, NAME, LOCATION, TIME_OPEN, TIME_CLOSED) \
            VALUES (?, ?, ?, ?, ?);""", canteens)
    CONNECTION.commit()
    print("The rest of the records created.")


def query_records():
    """
    Query records from database tables.
    """
    cursor = CONNECTION.execute("SELECT * FROM CANTEEN;")
    CONNECTION.commit()
    for row in cursor:
        print("ID ", row[0])
        print("PROVIDERID ", row[1])
        print("NAME ", row[2])
        print("LOCATION ", row[3])
        print("TIME_OPEN ", row[4])
        print("TIME_CLOSED ", row[5])
    print("End of query.")


def query_open_900_1620():
    """
    Query records for canteens which are open from 09.00 AM to 16.20 PM.
    """
    cursor = CONNECTION.cursor()
    cursor.execute(
        """SELECT NAME, TIME_OPEN, TIME_CLOSED FROM CANTEEN WHERE TIME_OPEN <= 900 AND TIME_CLOSED >= 1620;""")
    CONNECTION.commit()
    print("Canteens open from 09.00 AM until 16.20 PM:")
    for row in cursor:
        print(
            f"{row[0]} is open from {str(row[1])[:-2]}.{str(row[1])[-2:]} AM until {str(row[2])[:-2]}.{str(row[2])[-2:]} PM")
    print("End of query.")


def query_canteens_serviced_by():
    provider = 'Baltic Restaurants Estonia AS'
    cursor = CONNECTION.cursor()
    cursor.execute(
        """SELECT NAME FROM CANTEEN LEFT JOIN PROVIDER ON PROVIDER.ID=CANTEEN.PROVIDERID WHERE PROVIDERNAME=?;""", (provider,))
    CONNECTION.commit()
    print("Canteens serviced by Baltic Restaurants Estonia AS are:")
    for row in cursor:
        print(row[0])
    print("End of query.")


def delete_canteen() -> None:
    """
    Delete CANTEEN table from DINERS database.
    """
    CONNECTION.execute("""DROP TABLE CANTEEN""")
    print("Table CANTEEN successfully deleted.")


def delete_provider() -> None:
    """
    Delete PROVIDER table from DINERS database.
    """
    CONNECTION.execute("""DROP TABLE PROVIDER""")
    print("Table PROVIDER successfully deleted.")


def close_connection() -> None:
    """
    Close database connection.
    """
    CONNECTION.close()
    print("Database connection closed successfully")


if __name__ == "__main__":
    open_connection("DINERS.db")
    delete_canteen()
    delete_provider()
    create_provider()
    create_canteen()
    create_it_college_record()
    create_records_in_bulk()
    query_records()
    query_open_900_1620()
    query_canteens_serviced_by()
    close_connection()
