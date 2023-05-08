"""
This module contains queries to conduct against 
ALCHEMYDINERS database using SQLAlchemy ORM approach.

This module assumes that Provider, Canteen and Base classes are
described in sql_alchemy_models.py file and SQLite3 and
SQLAlchemy is installed.
In case exceptions text about the action not conducted will be
printed and all exeptions are forwarded as general exeptions.

Error and edge case handling is incomplete at the moment.

For running examples and printing results into console,
run this file from command line.

Available variables:
- engine - sqlite database engine

Available functions:
- def create_provider_table():
    -> Creates table PROVIDER into ALCHEMYDINERS database 
    if it does not exist already
- def create_canteen_table():
    -> Creates table CANTEEN into ALCHEMYDINERS database
    if it does not exist already.
- def create_all_tables():
    -> Creates all tables which are defined into ALCHEMYDINERS database
    simultaneously if they do not exist already.
- def add_one_record(rec: dict) -> dict:
    -> Creates a record into CANTEEN and if needed 
    into PROVIDER database tables.
- def add_multiple_records(diners: list) -> list:
    -> Create records in CANTEEN and PROVIDER tables
    based on the list of canteens given as dictionaries.
- def query_all_records(table: str) -> list | None:
    -> Selects all records from given table and returns
    them as a list of dictionaries.
- def select_open_between_inclusive(time_open: int,
    time_closed: int) -> list:
    -> Queries records for canteens which are open within
    given timeframe.
- def query_canteens_serviced_by(provider_to_query: str) -> list:
    -> Queries canteens serviced by given provider.
- def update_one(table: str, item_id: int,
    new_info: dict) -> dict | None:
    -> Updates one record in database table.
- def update_many(table: str, new_info: list) -> list | None:
    -> Updates multiple records simultaneously in given database table.
- def delete_one(table: str, item_id: int) -> dict | None:
    -> Delete one record from database table.
- def delete_many(table: str, item_ids: list) -> list | None:
    -> Deletes multiple records from given database table.
- def drop_provider_table():
    -> Deletes PROVIDER table from ALCHEMYDINERS database.
- def drop_canteen_table():
    -> Deletes CANTEEN table from ALCHEMYDINERS database.
- def drop_all_tables():
    -> Deletes all tables from ALCHEMYDINERS database.
"""

from sqlalchemy import create_engine, insert, select, update, delete
from sqlalchemy.orm import Session

from sql_alchemy_models import Provider, Canteen, Base

engine = create_engine("sqlite+pysqlite:///ALCHEMYDINERS.db",
                       echo=False)


def create_provider_table():
    """
    Create database table PROVIDER.

    Creates table PROVIDER into ALCHEMYDINERS database
    if it does not exist already.
    """

    try:
        Provider.__table__.create(engine, checkfirst=True)
        print("Table PROVIDER successfully created.")
    except Exception as expt:
        print("Table PROVIDER not created")
        raise expt


def create_canteen_table():
    """
    Create database table CANTEEN.

    Creates table CANTEEN into ALCHEMYDINERS database
    if it does not exist already.
    """

    try:
        Canteen.__table__.create(engine, checkfirst=True)
        print("Table CANTEEN successfully created.")
    except Exception as expt:
        print("Table CANTEEN not created")
        raise expt


def create_all_tables():
    """
    Create database table PROVIDER.

    Creates all tables which are defined into ALCHEMYDINERS database
    simultaneously if they do not exist already.
    """

    try:
        Base.metadata.create_all(engine, checkfirst=True)
        print("All tables successfully created.")
    except Exception as expt:
        print("No tables were created")
        raise expt


def add_one_record(rec: dict) -> dict:
    """
    Create records in CANTEEN and PROVIDER tables
    based on the record given.

    Given the canteen as a dictionary with keys:
    - ProviderName,
    - Name,
    - Location,
    - time-open,
    - time-closed,
    this function inserts it to database.
    :param rec: dictionary of a record to be inserted into a database
    :return Canteen instance as a dictionary
    """

    try:
        one_canteen = Canteen(provider=Provider(
            ProviderName=rec["ProviderName"]),
            Name=rec["Name"],
            Location=rec["Location"],
            time_open=rec["time_open"],
            time_closed=rec["time_closed"])
        session.add(one_canteen)
        # Flush all object changes into database
        session.flush()
        # Refresh object attributes
        session.refresh(one_canteen)
        print(f"Record created:\n{one_canteen}")
        return one_canteen.to_dict()
    except Exception as expt:
        session.rollback()
        raise expt


def add_multiple_records(diners: list) -> list:
    """
    Create records in CANTEEN and PROVIDER tables
    based on the list of canteens given.

    Given the canteen as a list of dictionaries with keys:
    - ProviderName,
    - Name,
    - Location,
    - time-open,
    - time-closed,
    this function inserts them into the database.
    Note:
    - In case there are case-wise multiple versions of a provider, the
    last in list will be inserted.
    - In case there are case-wise multiple versions of a
    canteen's name, they all are considered different and will be
    inserted as different records.
    - Matching Provider od Canteens already in db will not be
        inserted twice

    :param diners: list of dictionaries of a canteens to be inserted
        into a database

    :return list of Canteen instances as dictionaries
    """

    try:
        # Filter unique providers
        unique_providers = {provider["ProviderName"].casefold(
        ): provider["ProviderName"] for provider in diners}
        provider_names_to_insert = list(
            {"ProviderName": provider} for provider in unique_providers.values())

        # First add providers.
        # add_all method checks first the database and then
        # adds distinct records.
        # add_all does not merge duplicates currently already added or
        # to be added into session
        # that is why only unique provider names were filtered first
        session.add_all([Provider(
            ProviderName=provider["ProviderName"]) for provider
            in provider_names_to_insert])
        session.flush()

        # Alter the input by adding "ProviderID" key and select
        # clause as its value to retrieve provider info from db.
        # After that remove redundant keys which may trigger errors.
        for diner in diners:
            diner["ProviderID"] = select(Provider.ID).where(
                Provider.ProviderName ==
                unique_providers[diner["ProviderName"].casefold()])
            diner.pop("ProviderName")

        # Add canteens into db
        canteens_added = session.scalars(
            insert(Canteen).values(diners).returning(Canteen),
            execution_options={"populate_existing": True})
        # Iterating over canteens_added will clear them from session.
        # In order to use them multiple times, helper variable
        # can be used.
        result = list(canteens_added)
        result_to_return = [item.to_dict() for item in result]
        print(f"Canteens added:\n{result}")
        return result_to_return

    except Exception as expt:
        session.rollback()
        raise expt


def query_all_records(table: str) -> list | None:
    """
    Select all records from given table.

    Selects all records from given table and returns
    them as a list of dictionaries.
    Prints the result to the console.

    :param: table: database table to query info from
    :return list of records as dictionaries
    """

    try:
        match table:
            case "PROVIDER":
                table_to_query = Provider
            case "CANTEEN":
                table_to_query = Canteen
            case _:
                print(f"Could not find table {table}")
                return None
        results = session.execute(
            select(table_to_query).order_by(table_to_query.ID))
        results_list = list(results.scalars())
        print(f"All records in table {table} are:\n{results_list}")
        return [item.to_dict() for item in results_list]
    except Exception as expt:
        raise expt


def select_open_between_inclusive(time_open: int,
                                  time_closed: int) -> list:
    """
    Query records for canteens which are open within given timeframe.

    Queries from database table CANTEEN for canteens which are opened
    within given timeframe, prints out the names,
    open and closing times of
    items found and returns a list of dictionaries with following keys:
    - "ID"
    - "ProviderID"
    - "Name"
    - "Location"
    - "time_open"
    - "time_closed"
    - "provider": {
        "ID"
        "ProviderName"
    }

    :param time_open: the opening time of a canteen to query
    :param time_closed: the closing time of a canteen to query
    :return list of Canteen instances representations as dictionaries
    """

    query = select(Canteen).filter(Canteen.time_open <=
                                   time_open,
                                   Canteen.time_closed >= time_closed)

    results = session.execute(query)
    print("Canteens open from ", end="")
    print(f"{str(time_open)[:-2]}.{str(time_open)[-2:]} AM ", end="")
    print(f"until {str(time_closed)[:-2]}.{str(time_closed)[-2:]} PM:\n")

    # Helper variable for holding results info in order
    #  to use it multiple times.
    results_list = list(results.scalars())
    for diner in results_list:
        print(f"{diner.Name} is open")
        print(
            f"from {str(diner.time_open)[:-2]}.{str(diner.time_open)[-2:]} AM")
        print(
            f"until {str(diner.time_closed)[:-2]}.{str(diner.time_closed)[-2:]} PM")
        print(".  ." * 10)
    print("End of query.")
    return [result.to_dict() for result in results_list]


def query_canteens_serviced_by(provider_to_query: str) -> list:
    """
    Query canteens serviced by given provider.

    Queries from database ALCHEMYDINERS by combining info 
    from CANTEEN and PROVIDER tables
    for canteens which are serviced by provider given as an argument,
    prints out the names of canteens as a list and returns the
    canteens meeting the criteria as a list of dictionaries.

    :param provider_to_query: provider servicing canteens
    :return list of canteens as dictionaries
    """

    query = select(Canteen).join(Canteen.provider).where(
        Provider.ProviderName == provider_to_query)

    results = session.execute(query)

    # Helper variable for holding results info in order
    #  to use it multiple times.
    results_list = list(results.scalars())
    print(f"Canteens serviced by {provider_to_query} are:")
    for canteen in results_list:
        print(canteen.Name)
        print(".  ." * 10)
    print("End of query.")
    return [result.to_dict() for result in results_list]


def update_one(table: str, item_id: int, new_info: dict) -> dict | None:
    """
    Update one record in database table.

    Updates one record in one database table with new values given
    as a dictionary based on table name and record ID passed as
    arguments alongside new values.

    :param table: database table to update
    :param item_id: record ID which info will be updated
    :param new_info: dictionary with new info
    :return updated record as a dictionary
    """

    try:
        match table:
            case "PROVIDER":
                table_to_update = Provider
            case "CANTEEN":
                table_to_update = Canteen
            case _:
                print(f"Could not find table {table}")
                return None
        result = session.execute(update(table_to_update).where(
            table_to_update.ID == item_id).values(new_info)
            .returning(table_to_update)).scalars().one()
        print(f"Updated record in {table} is:\n{result}")
        return result.to_dict()
    except Exception as expt:
        session.rollback()
        raise expt


def update_many(table: str, new_info: list) -> list | None:
    """
    Update multiple records simultaneously in database table.

    Updates several records in one database table with new values given
    as a list of dictionaries.
    Note:
    - It is mandatory for dictionaries passed as arguments to
    contain record ID-s to target the records to update.

    :param table: database table to update
    :param new_info: list of dictionaries containing
        id-s and new info for records
    :return list of updated records as a dictionaries
    """

    try:
        match table:
            case "PROVIDER":
                table_to_update = Provider
            case "CANTEEN":
                table_to_update = Canteen
            case _:
                print(f"Could not find table {table}")
                return None
        session.execute(update(table_to_update), new_info,)
        updated_results = session.execute(select(table_to_update).where(
            table_to_update.ID.in_([data["ID"] for data in new_info])))
        result_to_return = list(updated_results.scalars())
        print(
            f"Updated records in table {table} are:\n{result_to_return}")
        return [item.to_dict() for item in result_to_return]
    except Exception as expt:
        session.rollback()
        raise expt


def delete_one(table: str, item_id: int) -> dict | None:
    """
    Delete one record in database table.

    Deletes one record from given database table based on
    id passed as an argument and returns the deleted item.

    :param table: database table to delete from
    :param item_id: ID of the records to be deleted
    :return deleted record
    """

    try:
        match table:
            case "PROVIDER":
                table_to_delete_from = Provider
            case "CANTEEN":
                table_to_delete_from = Canteen
            case _:
                print(f"Could not find table {table}")
                return None
        result = session.execute(delete(table_to_delete_from).where(
            table_to_delete_from.ID ==
            item_id).returning(table_to_delete_from)).scalars().one()
        print(f"Record deleted from table {table} is:\n{result}")
        return result.to_dict()
    except Exception as expt:
        session.rollback()
        raise expt


def delete_many(table: str, item_ids: list) -> list | None:
    """
    Delete several records simultaneously from database table.

    Deletes many records from given database table based on
    ID-s passed as a list and returns deleted items as a
    list of dictionaries.

    :param table: database table to delete from
    :param item_ids: list of ID-s of the records to be deleted
    :return deleted records as a list of dictionaries
    """

    try:
        match table:
            case "PROVIDER":
                table_to_delete_from = Provider
            case "CANTEEN":
                table_to_delete_from = Canteen
            case _:
                print(f"Could not find table {table}")
                return None
        result = session.execute(delete(table_to_delete_from).where(
            table_to_delete_from.ID.in_(
                item_ids)).returning(table_to_delete_from))
        result_list = result.scalars().all()
        print(f"Records deleted from table {table} are:\n{result_list}")
        return [result.to_dict() for result in result_list]
    except Exception as expt:
        session.rollback()
        raise expt


def drop_provider_table():
    """
    Delete PROVIDER table from ALCHEMYDINERS database.

    Drops database table PROVIDER.
    """

    Provider.__table__.drop(engine, checkfirst=True)


def drop_canteen_table():
    """
    Delete CANTEEN table from ALCHEMYDINERS database.

    Drops database table CANTEEN.
    """

    Canteen.__table__.drop(engine, checkfirst=True)


def drop_all_tables():
    """
    Delete all tables from ALCHEMYDINERS database.

    Drops all database tables.
    """

    Base.metadata.drop_all(engine, checkfirst=True)


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
    drop_canteen_table()
    drop_provider_table()
    # drop_all_tables()
    print("--*--" * 10)
    create_provider_table()
    create_canteen_table()
    print("--*--" * 10)

    # All function calls besides creating and dropping tables
    # must be made within session context.
    # Following code includes multiples samples you can uncomment
    # to try out the code.
    with Session(engine) as session, session.begin():
        one_test_record = add_one_record(record)
        # print("TEST1:\n", one_test_record)
        # print("TEST2:\n", one_test_record["Location"])
        print("--*--" * 10)
        multiple_test_records = add_multiple_records(canteens)
        # print("TEST3:\n", multiple_test_records)
        # print("TEST4:\n", multiple_test_records[3]["Name"])
        print("--*--" * 10)
        # all_providers = query_all_records("PROVIDER")
        # print("TEST5:\n", all_providers)
        # print("TEST6:\n", all_providers[1]["ProviderName"])
        # all_canteens = query_all_records("CANTEEN")
        # print("TEST7:\n", all_canteens)
        # print("TEST8:\n", all_canteens[4]["Name"])
        print("--*--" * 10)
        query_test_times = select_open_between_inclusive(900, 1620)
        # print("TEST9:\n", query_test_times)
        # print("TEST10:\n", query_test_times[3]["Name"])
        print("--*--" * 10)
        query_test_provider = query_canteens_serviced_by(
            "Baltic Restaurants Estonia AS")
        # print("TEST11:\n", query_test_provider)
        # print("TEST12:\n", query_test_provider[0]["ID"])
        print("--*--" * 10)
        update_provider = update_one(
            "PROVIDER", 2, {"ProviderName": "Rahva Toit"})
        # print("TEST13:\n", update_provider)
        update_canteen = update_one(
            "CANTEEN", 6, {"Location": "Presidendi kodu"})
        # print("TEST13:\n", update_provider)
        print("--*--" * 10)
        update_several_providers = update_many(
            "PROVIDER", [{"ID": 1, "ProviderName": "Sööklatädi"},
                         {"ID": 4, "ProviderName": "Kokapoiss"}])
        # print("TEST14:\n", update_several_providers[0]["ProviderName"])
        print("--*--" * 10)
        update_several_canteens = update_many(
            "CANTEEN", [{"ID": 3, "Name": "Tühi kõht"},
                        {"ID": 6, "Name": "Kuus kaalikat"},
                        {"ID": 9, "Name": "Pontšik ja pool praadi"}])
        # print("TEST15:\n", update_several_canteens[2]["Name"])
        print("--*--" * 10)
        # delete_one_provider = delete_one("PROVIDER", 4)
        # print("TEST16:\n", delete_one_provider)
        print("--*--" * 10)
        # Deleting several providers and canteens simultaneously is not
        # implemented yet.
        # delete_several_providers = delete_many("PROVIDER", [2, 3])
        # print("TEST17:\n", delete_several_providers)
        print("--*--" * 10)
        delete_several_canteens = delete_many("CANTEEN", [2, 4, 6, 8])
        # print("TEST18:\n", delete_several_canteens)
        print("--*--" * 10)
        print("X" * 40)
        print("*" * 40)

    # Engine disposal after the program has finished.
    # Do not delete this line.
    engine.dispose()
