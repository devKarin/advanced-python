"""
This module defines database schema for SQLite
database using SQLAlchemy ORM approach.

Available variables:
- engine - sqlite database engine

Available classes:
- class Base(DeclarativeBase):
    -> Declarative base class for declarative mapping.; no methods available
- class Provider(Base):
    -> ORM Mapped Provider class.
    Provider class has following class attributes:
    - __tablename__ - attribute referring to Table object instance name.
    - ID - primary key for Provider,
    - ProviderName - name of the provider,
    - canteens - related records in CANTEEN table
    Available methods in Provider class:
        - def __repr__(self) -> str:
        -> Provider class string representation.
        - def to_dict(self) -> dict:
        -> Cast the Provider instance into a dictionary.
- class Canteen(Base):
    -> ORM Mapped Canteen class.
    Canteen class has following class attributes:
    - __tablename__ - attribute referring to Table object instance name.
    - ID - primary key for Canteen,
    - ProviderID - foreign key referring to ID in PROVIDER table,
    - Name - the name of the Canteen instance,
    - Location - address of the canteen,
    - time_open - opening time of the canteen,
    - time_closed - closing time of the canteen,
    - provider - refers to related record in PROVIDER table
    Available methods in Canteen class:
    - def __repr__(self) -> str:
    -> Canteen class string representation.
    - def to_dict(self) -> dict:
    -> Cast the Canteen instance into a dictionary.
"""


from typing import Optional, List

from sqlalchemy import create_engine, String, Integer, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

engine = create_engine("sqlite+pysqlite:///ALCHEMYDINERS.db", echo=False)


class Base(DeclarativeBase):
    """
    Declarative base class for declarative mapping.

    The DeclarativeBase superclass supersedes the use of the
    declarative_base() function and
    registry.generate_base() methods in SQLAlchemy version 2.0.
    """


class Provider(Base):
    """
    ORM Mapped Provider class.

    Provider class refers to a Table object 
    named by __tablename__ attribute.
    Table is available via __table_ attribute.

    Other attributes Provider class has:
    - ID type of integer acting as a primary key for Provider,
    - ProviderName - a string representing the name of the provider,
    - canteens - refers to related records in CANTEEN table
    """

    __tablename__ = "PROVIDER"

    ID: Mapped[int] = mapped_column(primary_key=True, autoincrement="auto")
    ProviderName: Mapped[str] = mapped_column(String, unique=True)
    canteens: Mapped[List["Canteen"]] = relationship(
        back_populates="provider", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        """Provider class string representation."""
        return f"ID: {self.ID}\nProviderName: {self.ProviderName}\n"

    def to_dict(self) -> dict:
        """
        Cast the Provider instance into a dictionary.

        Casts Provider instance into a dictionary where the keys are most
        commonly used attributes.
        This method can be useful when the built-in __dict__ method can not
        be used (for example session-related issues in SQLAlchemy ORM).

        Structure:
        {
            "ID": self.ID,
            "ProviderName": self.ProviderName,
            "canteens":
            [
                {
                    "ID": canteen.ID,
                    "ProviderID": canteen.ProviderID,
                    "Name": canteen.Name,
                    "Location": canteen.Location,
                    "time_open": canteen.time_open,
                    "time_closed": canteen.time_closed,
                } for canteen in self.canteens
            ]
        }

        :param:
        :return dictionary with most needed attributes and their values
        """

        output = {
            "ID": self.ID,
            "ProviderName": self.ProviderName,
            "canteens":
            [
                {
                    "ID": canteen.ID,
                    "ProviderID": canteen.ProviderID,
                    "Name": canteen.Name,
                    "Location": canteen.Location,
                    "time_open": canteen.time_open,
                    "time_closed": canteen.time_closed,
                } for canteen in self.canteens
            ]
        }
        return output


class Canteen(Base):
    """
    ORM Mapped Canteen class.

    Canteen class refers to a Table object 
    named by __tablename__ attribute.
    Table is available via __table_ attribute.

    Other attributes Canteen class has:
    - ID, non-nullable, type of integer acting as a primary key for Canteen,
    - ProviderID, non-nullable, type of integer acting as a foreign key
    and referring to ID in PROVIDER table,
    - Name - a non-nullable string representing the name of the canteen,
    - Location - a string representing the address of the canteen,
    - time_open - an integer representing the opening time of the canteen,
    - time_closed - an integer representing the closing time of the canteen,
    - provider - refers to related record in PROVIDER table
    """

    __tablename__ = "CANTEEN"
    ID: Mapped[int] = mapped_column(primary_key=True, autoincrement="auto")
    ProviderID: Mapped[int] = mapped_column(
        ForeignKey("PROVIDER.ID"))
    Name: Mapped[str] = mapped_column(String)
    Location: Mapped[Optional[str]] = mapped_column(String)
    time_open: Mapped[int] = mapped_column(Integer)
    time_closed: Mapped[int] = mapped_column(Integer)
    provider: Mapped["Provider"] = relationship(
        back_populates="canteens", cascade="all")

    def __repr__(self) -> str:
        """Canteen class string representation."""

        output_string = f"\nID: {self.ID}," + \
            "\nprovider:" + \
            f"\n    ProviderID: {self.ProviderID}," + \
            f"\n    ProviderName: {self.provider.ProviderName}," + \
            f"\nName: {self.Name}," + f"\nLocation: {self.Location}," + \
            f"\ntime_open: {self.time_open}," + \
            f"\ntime_closed: {self.time_closed}\n"
        return output_string

    def to_dict(self) -> dict:
        """
        Cast the Canteen instance into a dictionary.

        Casts Canteen instance into a dictionary where the keys are most
        commonly used attributes.
        This method can be useful when the built-in __dict__ method can not
        be used (for example session-related issues in SQLAlchemy ORM).
        Structure:
        {
            "ID": self.ID,
            "ProviderID": self.ProviderID,
            "Name": self.Name,
            "Location": self.Location,
            "time_open": self.time_open,
            "time_closed": self.time_closed,
            "provider": {
                "ID": self.provider.ID, 
                "ProviderName": self.provider.ProviderName
            }
        }

        :param:
        :return dictionary with most needed attributes and their values
        """

        output = {
            "ID": self.ID,
            "ProviderID": self.ProviderID,
            "Name": self.Name,
            "Location": self.Location,
            "time_open": self.time_open,
            "time_closed": self.time_closed,
            "provider": {
                "ID": self.provider.ID,
                "ProviderName": self.provider.ProviderName
            }
        }
        return output


if __name__ == "__main__":
    pass
