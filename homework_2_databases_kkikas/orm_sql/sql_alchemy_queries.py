"""
This module contains queries to conduct against ALCHEMYDINERS database.
"""

from sqlalchemy import insert, select
from sqlalchemy.orm import Session

from sql_alchemy_models import Provider, Canteen, engine


def add_one_record(rec: dict) -> None:
    """
    Create records in CANTEEN and PROVIDER tables
    according to the canteen located in IT-College.
    """
    with Session(engine) as session, session.begin():
        try:
            it_college_canteen = Canteen(provider=Provider(ProviderName=rec["ProviderName"]),
                                         Name=rec["Name"],
                                         Location=rec["Location"],
                                         time_open=rec["time_open"], time_closed=rec["time_closed"])
            session.add(it_college_canteen)
        except:
            session.rollback()
            raise


def add_multiple_records(diners: list) -> None:
    """
    Create records in CANTEEN and PROVIDER tables
    according to the canteen located in IT-College.
    """
    unique_providers = {}
    providers = [provider["ProviderName"]
                 for provider in diners]

    for name in providers:
        if name.casefold() not in unique_providers:
            unique_providers[name.casefold()] = name
        else:
            continue

    providers = list({"ProviderName": provider}
                     for provider in unique_providers.values())
    with Session(engine) as session, session.begin():
        try:
            returned_providers = session.scalars(insert(Provider).returning(
                Provider), providers,)
            provider_ids = {
                provider.ProviderName.casefold(): provider.ID for provider in returned_providers}
            for diner in diners:
                if diner["ProviderName"].casefold() in provider_ids:
                    diner["ProviderID"] = provider_ids[diner["ProviderName"].casefold()]
        except:
            session.rollback()
            raise

    with Session(engine) as session, session.begin():
        try:
            session.execute(insert(Canteen), diners,)
        except:
            session.rollback()
            raise


def select_open_between_inclusive(time_open: int, time_closed: int):
    query = select(Canteen).filter(Canteen.time_open <=
                                   time_open, Canteen.time_closed >= time_closed)
    with Session(engine) as session:
        results = session.execute(query)
        print("Canteens open from ", end="")
        print(f"{str(time_open)[:-2]}.{str(time_open)[-2:]} AM ", end="")
        print(f"until {str(time_closed)[:-2]}.{str(time_closed)[-2:]} PM:\n")

        for canteen in results.scalars():
            print(f"{canteen.Name} is open")
            print(
                f"from {str(canteen.time_open)[:-2]}.{str(canteen.time_open)[-2:]} AM")
            print(
                f"until {str(canteen.time_closed)[:-2]}.{str(canteen.time_closed)[-2:]} PM")
            print(".  ." * 10)
        print("End of query.")


def query_canteens_serviced_by(provider_to_query: str) -> str:
    query = select(Canteen).join(Canteen.provider).where(
        Provider.ProviderName == provider_to_query)
    with Session(engine) as session:
        results = session.execute(query)
        print(f"Canteens serviced by {provider_to_query} are:")
        for canteen in results.scalars():
            print(canteen.Name)
            print(".  ." * 10)
        print("End of query.")


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
    # delete_table(Canteen)
    # delete_table(Provider)
    add_one_record(record)
    print("--*--" * 10)
    add_multiple_records(canteens)
    print("--*--" * 10)
    select_open_between_inclusive(900, 1620)
    print("--*--" * 10)
    query_canteens_serviced_by("Baltic Restaurants Estonia AS")
    print("--*--" * 10)
    print("X" * 40)
    print("*" * 40)
