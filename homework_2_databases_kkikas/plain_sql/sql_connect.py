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
        ProviderName TEXT UNIQUE NOT NULL);""")
    print("Table PROVIDER successfully created.")


def create_canteen() -> None:
    """
    Create database table named CANTEEN.
    """
    CONNECTION.execute("""CREATE TABLE IF NOT EXISTS CANTEEN
        (ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        ProviderID INT NOT NULL,
        Name TEXT NOT NULL,
        Location TEXT,
        time_open SMALLINT NOT NULL,
        time_closed SMALLINT NOT NULL,
        FOREIGN KEY (ProviderID) REFERENCES PROVIDER (ID)
        ON UPDATE CASCADE
        ON DELETE SET NULL);""")
    print("Table CANTEEN successfully created.")


def insert_one_record(rec: dict) -> None:
    """
    Create records in CANTEEN and PROVIDER tables
    according to the canteen located in IT-College.
    """
    CONNECTION.execute("""PRAGMA foreign_keys = ON;""")
    CONNECTION.execute("""INSERT INTO PROVIDER\
                       (ProviderName)\
                       VALUES\
                       (:provider_name)""", (rec["ProviderName"],))
    CONNECTION.execute("""INSERT INTO CANTEEN\
                       (ProviderID, Name, Location,\
                       time_open, time_closed)\
                       VALUES\
                       ((SELECT ID FROM PROVIDER \
                        WHERE ProviderName=:provider_name),\
                            :name, :location,\
                                :open, :closed)""", (
        rec["ProviderName"], rec["Name"], rec["Location"],
        rec["time_open"], rec["time_closed"]
    ))
    CONNECTION.commit()
    print("IT College record created.")


def insert_records_in_bulk(diners: list) -> None:
    """
    Create records in CANTEEN and PROVIDER tables
    for canteens other than the one located in IT-College.
    """

    unique_providers = {}
    providers = [provider["ProviderName"]
                 for provider in diners]

    for name in providers:
        if name.casefold() not in unique_providers:
            unique_providers[name.casefold()] = name
        else:
            continue

    providers = tuple({"name": provider}
                      for provider in unique_providers.values())

    cursor = CONNECTION.cursor()
    cursor.executemany(
        """INSERT OR REPLACE INTO PROVIDER (ProviderName) VALUES(:name);""", providers)

    for i, element in enumerate(diners):
        provider_name = (element["ProviderName"],)
        result = cursor.execute(
            "SELECT ID FROM PROVIDER WHERE ProviderName=? COLLATE NOCASE;", provider_name)
        res = [row[0] for row in result][0]
        # Replace provider name with id.
        element["ProviderName"] = res

    CONNECTION.executemany(
        """INSERT INTO CANTEEN (ProviderID, Name, Location, time_open, time_closed) \
            VALUES (?, ?, ?, ?, ?);""", [tuple(diner.values()) for diner in diners])
    CONNECTION.commit()
    print("The rest of the records created.")


def query_records() -> list:
    """
    Query records from database tables.
    """
    cursor = CONNECTION.execute("SELECT * FROM CANTEEN;")
    CONNECTION.commit()
    for row in cursor:
        print("ID: ", row[0])
        print("ProviderID: ", row[1])
        print("Name: ", row[2])
        print("Location: ", row[3])
        print("time_open: ", row[4])
        print("time_closed: ", row[5])
        print(".  ." * 10)
    print("End of query.")
    return cursor


def query_open_between_inclusive(time_open: int, time_closed: int) -> list:
    """
    Query records for canteens which are open from 09.00 AM to 16.20 PM.
    """
    cursor = CONNECTION.cursor()
    cursor.execute(
        """SELECT Name, time_open, time_closed FROM CANTEEN WHERE \
            time_open <= :time_open AND time_closed >= :time_closed;""",
        (time_open, time_closed))
    CONNECTION.commit()
    print("Canteens open from ", end="")
    print(f"{str(time_open)[:-2]}.{str(time_open)[-2:]} AM ", end="")
    print(f"until {str(time_closed)[:-2]}.{str(time_closed)[-2:]} PM:\n")
    for row in cursor:
        print(f"{row[0]} is open")
        print(f"from {str(row[1])[:-2]}.{str(row[1])[-2:]} AM")
        print(f"until {str(row[2])[:-2]}.{str(row[2])[-2:]} PM")
        print(".  ." * 10)
    print("End of query.")
    return list(cursor)


def query_canteens_serviced_by(provider: str) -> str:
    """
    Query canteens serviced by provider given as and argument.
    """
    cursor = CONNECTION.cursor()
    cursor.execute(
        """SELECT NAME FROM CANTEEN LEFT JOIN PROVIDER ON \
            PROVIDER.ID=CANTEEN.ProviderID WHERE ProviderName=?;""", (provider,))
    CONNECTION.commit()
    print(f"Canteens serviced by {provider} are:")
    result = ""
    for row in cursor:
        result = row[0]
        print(row[0])
        print(".  ." * 10)
    print("End of query.")
    return result


def delete_canteen() -> None:
    """
    Delete CANTEEN table from DINERS database.
    """
    CONNECTION.execute("""DROP TABLE CANTEEN""")
    print("Table CANTEEN deleted successfully.")


def delete_provider() -> None:
    """
    Delete PROVIDER table from DINERS database.
    """
    CONNECTION.execute("""DROP TABLE PROVIDER""")
    print("Table PROVIDER deleted successfully.")


def close_connection() -> None:
    """
    Close database connection.
    """
    CONNECTION.close()
    print("Database connection successfully closed.")


if __name__ == "__main__":
    record = {
        "ProviderName": "Bitt OÜ",
        "Name": "bitStop KOHVIK",
        "Location": "IT College, Raja 4c",
        "time_open": 900,
        "time_closed": 1600
    }
    canteens = [
        {
            "ProviderName": "Rahva Toit",
            "Name": "Economics- and social science building canteen",
            "Location": "Akadeemia tee 3, SOC- building",
            "time_open": 830,
            "time_closed": 1830
        },
        {
            "ProviderName": "Rahva Toit",
            "Name": "Library canteen",
            "Location": "Akadeemia tee 1/Ehitajate tee 7",
            "time_open": 830,
            "time_closed": 1900
        },
        {
            "ProviderName": "Baltic Restaurants Estonia AS",
            "Name": "Main building Deli cafe",
            "location": "Ehitajate tee 5, U01 building",
            "time_open": 900,
            "time_closed": 1630
        },
        {
            "ProviderName": "Baltic Restaurants Estonia AS",
            "Name": "Main building Daily lunch restaurant",
            "Location": "Ehitajate tee 5, U01 building",
            "time_open": 900,
            "time_closed": 1630
        },
        {
            "ProviderName": "Rahva toit",
            "Name": "U06 building canteen",
            "Location": "",
            "time_open": 900,
            "time_closed": 1600
        },
        {
            "ProviderName": "Baltic Restaurants Estonia AS",
            "Name": "Natural Science building canteen",
            "Location": "Akadeemia tee 15, SCI building",
            "time_open": 900,
            "time_closed": 1600
        },
        {
            "ProviderName": "Baltic Restaurants Estonia AS",
            "Name": "ICT building canteen",
            "Location": "Raja 15/Mäepealse 1",
            "time_open": 900,
            "time_closed": 1600
        },
        {
            "ProviderName": "TTÜ Sport OÜ",
            "Name": "Sports building canteen",
            "Location": "Männiliiva 7, S01 building",
            "time_open": 1100,
            "time_closed": 2000
        }
    ]

    open_connection("DINERS.db")
    print("--*--" * 10)
    delete_canteen()
    delete_provider()
    print("--*--" * 10)
    create_provider()
    print("--*--" * 10)
    create_canteen()
    print("--*--" * 10)
    insert_one_record(record)
    print("--*--" * 10)
    insert_records_in_bulk(canteens)
    print("--*--" * 10)
    query_records()
    print("--*--" * 10)
    query_open_between_inclusive(900, 1620)
    print("--*--" * 10)
    query_canteens_serviced_by("Baltic Restaurants Estonia AS")
    print("--*--" * 10)
    close_connection()
    print("X" * 40)
    print("*" * 40)
