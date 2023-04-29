"""
This module creates a database and provides actions on its tables.

The database DINERS has two related tables CANTEEN and PROVIDER.
Available functions:
- def open_connection(d_base="DINERS.db") -> sqlite3.Connection:
    -> Creates database connection.
- def create_provider(connection: sqlite3.Connection) -> None:
    -> Creates database table named PROVIDER which contains
    information about canteen providers in TalTech's buildings.
- def create_canteen(connection: sqlite3.Connection) -> None:
    -> Creates database table named CANTEEN which contains
    information about canteens in TalTech's buildings.
- def insert_one_record(connection: sqlite3.Connection, rec: dict) -> dict:
    -> Creates a record in CANTEEN and PROVIDER tables,
    returns created record as a dictionary.
- def insert_records_in_bulk(connection: sqlite3.Connection, diners: list) -> list:
    -> Creates records in CANTEEN and PROVIDER tables
    based on list of canteens as dictionaries provided,
    returns inserted data as a list of dictionaries.
- def query_all_records(connection: sqlite3.Connection, \
    table: str) -> list | None:
    -> Selects all records from given database table
    and returns them as a list of dictionaries.
- def query_open_between_inclusive(connection: sqlite3.Connection, \
    time_open: int, time_closed: int) -> list:
    -> Selects records for canteens which are open within given timeframe
    from database and returns a list with canteen names matching criteria
    and opening and closing time.
- def query_canteens_serviced_by(connection: sqlite3.Connection, \
    provider: str) -> list:
    -> Selects canteens serviced by given provider from database and
    returns them as a list of canteen names.
- def drop_canteen(connection: sqlite3.Connection) -> None:
    -> Deletes CANTEEN datatable from database.
- def drop_provider(connection: sqlite3.Connection) -> None:
    -> Deletes PROVIDER datatable from database.
- def close_connection(connection: sqlite3.Connection) -> None:
    Closes sqlite database connection.
"""


import sqlite3


def open_connection(d_base="DINERS.db") -> sqlite3.Connection:
    """
    Create database connection.

    :param d_base: database file name as a string,
        defaults to "DINERS.db"
    :return: Connection to the database
    """

    try:
        connection = sqlite3.connect(d_base)
        print("Database opened successfully")
    except Exception as expt:
        print("Connecting with database failed.")
        raise expt
    return connection


def create_provider(connection: sqlite3.Connection) -> None:
    """
    Create database table named PROVIDER.

    PROVIDER has columns ID and ProviderName.
    ID is autoincrement integer primary key,
    ProviderName is a unique non-nullable string marking
    the name of the company.

    :param connection: connection to the database
    :return None
    """

    try:
        connection.execute("""CREATE TABLE IF NOT EXISTS PROVIDER
            (ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            ProviderName TEXT UNIQUE NOT NULL);""")
        connection.commit()
        print("Table PROVIDER successfully created.")
    except Exception as expt:
        connection.rollback()
        print("Provider not created")
        raise expt


def create_canteen(connection: sqlite3.Connection) -> None:
    """
    Create database table named CANTEEN.

    CANTEEN has following columns:\n
    ID - non-nullable autoincrement integer, which acts as a primary key,
    ProviderID - an integer which acts as a foreign key and
    refers to ID column in PROVIDER table, 
    Name - non-nullable text,
    Location - text,
    time-open - non-nullable integer indicating the canteen opening time,
    time-closed - non-nullable integer indicating the canteen closing time.

    On update of PROVIDER table the key changes propagate to CANTEEN
    table, on delete the values are set to be NULL.

    :param connection: connection to the database
    :return None
    """

    try:
        connection.execute("""CREATE TABLE IF NOT EXISTS CANTEEN
            (ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            ProviderID INT,
            Name TEXT NOT NULL,
            Location TEXT,
            time_open INT NOT NULL,
            time_closed INT NOT NULL,
            FOREIGN KEY (ProviderID) REFERENCES PROVIDER (ID)
            ON UPDATE CASCADE
            ON DELETE SET NULL);""")
        connection.commit()
        print("Table CANTEEN successfully created.")
    except Exception as expt:
        connection.rollback()
        print("Canteen not created")
        raise expt


def insert_one_record(connection: sqlite3.Connection, rec: dict) -> dict:
    """
    Create a record in CANTEEN and PROVIDER tables.

    Takes a dictionary with keys 
        "ProviderName", "Name", "Location", "time_open", "time_closed"
    as an argument and returns inserted data as dictionary with keys
         "ID", "ProviderID", "Name", "Location", "time_open", "time_closed", "ProviderName".

    :param connection: connection to the database
    :param rec: record to be inserted as dictionary
    :return: Dictionary with data inserted
    """

    keys = ["ID", "ProviderID", "Name",
            "Location", "time_open", "time_closed"]
    try:
        connection.execute("""PRAGMA foreign_keys = ON;""")
        provider_record = connection.execute("""INSERT INTO PROVIDER\
                        (ProviderName)\
                        VALUES\
                        (:provider_name) RETURNING ProviderName;""", (rec["ProviderName"],))
        canteen_record = connection.execute("""INSERT INTO CANTEEN\
                        (ProviderID, Name, Location,\
                        time_open, time_closed)\
                        VALUES\
                        ((SELECT ID FROM PROVIDER \
                            WHERE ProviderName=:provider_name),\
                                :name, :location,\
                                    :open, :closed) RETURNING *;""", (
            rec["ProviderName"], rec["Name"], rec["Location"],
            rec["time_open"], rec["time_closed"]
        ))

        canteen = canteen_record.fetchall()
        provider = provider_record.fetchall()
        connection.commit()
        result = dict(zip(keys, canteen[0]))
        result["ProviderName"] = provider[0][0]
        print(f"Record created:\n {result}")
    except Exception as expt:
        connection.rollback()
        print("Record not created")
        raise expt
    return result


def insert_records_in_bulk(connection: sqlite3.Connection, diners: list) -> list:
    """
    Create records in CANTEEN and PROVIDER tables
    for canteens provided as list of dictionaries.

    Takes a list of dictionaries with keys 
        "ProviderName", "Name", "Location", 
        "time_open", "time_closed"
    as an argument and returns inserted data as a list
    of dictionaries with keys
         "ID", "ProviderID", "Name", "Location", 
         "time_open", "time_closed", "ProviderName".

    :param connection: connection to the database
    :param diners: list of records as dictionaries to be
        inserted into database
    :return: List of dictionaries with inserted data
    """

    try:
        cursor = connection.cursor()
        keys = ["ID", "ProviderID", "Name",
                "Location", "time_open", "time_closed", "ProviderID", "ProviderName"]
        diner_names = [diner["Name"] for diner in diners]
        # Select unique providers, capitalisation doesn't matter.
        unique_providers = {provider["ProviderName"].casefold(
        ): provider["ProviderName"] for provider in diners}
        # Collect unique providers into a tuple of dictionaries.
        providers = tuple({"ProviderName": provider}
                          for provider in unique_providers.values())
        # Insert new providers.
        cursor.executemany(
            """INSERT OR REPLACE INTO PROVIDER (ProviderName) \
                VALUES(:ProviderName);""", providers)
        # Insert new diners.
        cursor.executemany(
            """INSERT INTO CANTEEN (\
                ProviderID, Name, Location, time_open, time_closed) \
                    VALUES ((SELECT ID AS ProviderID FROM PROVIDER \
                        WHERE ProviderName=:ProviderName COLLATE NOCASE), \
                            :Name, :Location, :time_open, :time_closed);""",
            diners)

        connection.commit()
        print("New records inserted:")
        # Create dynamically the amount of placeholders into the query string.
        query_string = f"SELECT * FROM CANTEEN LEFT JOIN PROVIDER \
            ON PROVIDER.ID=CANTEEN.ProviderID WHERE Name IN \
                ({'?, ' * (len(diner_names)-1) + '?'})"
        # Query the last inserted canteens
        inserted_result = cursor.execute(query_string, tuple(diner_names))
        # Make a dictionary to return results.
        result = [dict(zip(keys, item)) for item in inserted_result.fetchall()]
        print(result)
        connection.commit()
        print("End of query.")
    except Exception as expt:
        connection.rollback()
        print("Records not created")
        raise expt
    return result


def query_all_records(connection: sqlite3.Connection, table: str) -> list | None:
    """
    Query all records from database tables.

    Returns all records from given table.

    :param connection: connection to the database
    :param table: name of database table to query
    :return list of records as dictionaries with keys
        "ID", "ProviderID", "Name", "Location", "time_open",
        "time_closed", "ProviderID", "ProviderName"
        or None in case of an undefined query.
    """

    try:
        keys = ["ID", "ProviderID", "Name", "Location", "time_open",
                "time_closed", "ProviderID", "ProviderName"]
        if table == "CANTEEN":
            cursor = connection.execute("SELECT * FROM CANTEEN;")
            result = [dict(zip(keys, item)) for item in cursor.fetchall()]
            print(result)
        elif table == "PROVIDER":
            cursor = connection.execute("SELECT * FROM PROVIDER;")
            result = [dict(zip(["ID", "ProviderName"], item))
                      for item in cursor.fetchall()]
        else:
            print(f"There are no queries for table {table} defined.")
            return None
        formatted_result = ""
        for item in result:
            formatted_result += "\n"
            for key, value in item.items():
                formatted_result += f"{key}: {value}\n"
            formatted_result += "\n" + (".  ." * 10) + "\n"
        print(formatted_result)
        print("End of query.")
        connection.commit()
        return result
    except Exception as expt:
        print("Fetching records failed")
        raise expt


def query_open_between_inclusive(connection: sqlite3.Connection,
                                 time_open: int, time_closed: int) -> list:
    """
    Query records for canteens which are open within given timeframe.

    Queries from database table CANTEEN for canteens which are opened
    within given timeframe and returns a list of tuples containing
    canteen names matching criteria, opening time and closing time.
    :param connection: connection to the database
    :param time_open: the opening time of a canteen to query
    :param time_closed: the closing time of a canteen to query
    :return list of tuples containing canteen name, opening time and
        closing time
    """

    try:
        cursor = connection.cursor()
        cursor.execute(
            """SELECT Name, time_open, time_closed FROM CANTEEN WHERE \
                time_open <= ? AND time_closed >= ?;""",
            (time_open, time_closed))
        connection.commit()
        print("Canteens open from ", end="")
        print(f"{str(time_open)[:-2]}.{str(time_open)[-2:]} AM ", end="")
        print(f"until {str(time_closed)[:-2]}.{str(time_closed)[-2:]} PM:\n")
        result = cursor.fetchall()
        print(result)
        for row in result:
            print(f"{row[0]} is open")
            print(f"from {str(row[1])[:-2]}.{str(row[1])[-2:]} AM")
            print(f"until {str(row[2])[:-2]}.{str(row[2])[-2:]} PM")
            print(".  ." * 10)
        print("End of query.")
    except Exception as expt:
        print("Fetching records failed")
        raise expt
    return result


def query_canteens_serviced_by(connection: sqlite3.Connection, provider: str) -> list:
    """
    Query canteens serviced by given provider.

    Queries from database DINERS by combining info 
    from CANTEEN and PROVIDER tables
    for canteens which are serviced by provider given as an argument
    and returns the names of canteens as a list.

    :param connection: connection to the database
    :param provider: provider servicing canteens
    :return list of canteen names
    """

    try:
        cursor = connection.cursor()
        cursor.execute(
            """SELECT NAME FROM CANTEEN LEFT JOIN PROVIDER ON \
                PROVIDER.ID=CANTEEN.ProviderID WHERE ProviderName=?;""", (provider,))
        connection.commit()
        print(f"Canteens serviced by {provider} are:")
        result = [row[0] for row in cursor.fetchall()]
        for row in result:
            print(row)
            print(".  ." * 10)
        print("End of query.")
    except Exception as expt:
        print("Fetching records failed")
        raise expt
    return result


def drop_canteen(connection: sqlite3.Connection) -> None:
    """
    Delete CANTEEN table from DINERS database.

    Drops database table CANTEEN.

    :param connection: connection to the database
    :return
    """

    connection.execute("""DROP TABLE CANTEEN""")
    print("Table CANTEEN deleted successfully.")


def drop_provider(connection: sqlite3.Connection) -> None:
    """
    Delete PROVIDER table from DINERS database.

    Drops database table PROVIDER.

    :param connection: connection to the database
    :return
    """

    connection.execute("""DROP TABLE PROVIDER""")
    print("Table PROVIDER deleted successfully.")


def close_connection(connection: sqlite3.Connection) -> None:
    """
    Close database connection.

    Closes sqlite database connection.
    :param connection: connection to the database
    :return
    """

    connection.close()
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
            "Location": "Ehitajate tee 5, U01 building",
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

    DB = "DINERS.db"
    conn = open_connection(DB)
    print("--*--" * 10)
    drop_canteen(conn)
    drop_provider(conn)
    print("--*--" * 10)
    create_provider(conn)
    print("--*--" * 10)
    create_canteen(conn)
    print("--*--" * 10)
    insert_one_record(conn, record)
    print("--*--" * 10)
    insert_records_in_bulk(conn, canteens)
    print("--*--" * 10)
    query_all_records(conn, "CANTEEN")
    print("--*--" * 10)
    query_open_between_inclusive(conn, 900, 1620)
    print("--*--" * 10)
    query_canteens_serviced_by(conn, "Baltic Restaurants Estonia AS")
    print("--*--" * 10)
    close_connection(conn)
    print("X" * 40)
    print("*" * 40)
