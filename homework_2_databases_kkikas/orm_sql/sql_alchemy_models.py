"""
Module for operating SQLite databases using ORM.

"""


from typing import Optional, List

from sqlalchemy import create_engine, String, SmallInteger, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

engine = create_engine("sqlite+pysqlite:///ALCHEMYDINERS.db", echo=True)


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
    Table os available via __table_ attribute.
    """
    __tablename__ = "PROVIDER"

    ID: Mapped[int] = mapped_column(primary_key=True)
    ProviderName: Mapped[str] = mapped_column(String)
    canteens: Mapped[List["Canteen"]] = relationship(
        back_populates="provider", cascade="all, delete-orphan")
    sqlite_autoincrement = True

    def __repr__(self) -> str:
        """Provider class string representation."""
        return f"ID: {self.ID}\nProviderName: {self.ProviderName}\n"


class Canteen(Base):
    """
    ORM Mapped Canteen class.
    """
    __tablename__ = "CANTEEN"
    ID: Mapped[int] = mapped_column(primary_key=True)
    ProviderID = mapped_column(ForeignKey("PROVIDER.ID"))
    Name: Mapped[str] = mapped_column(String)
    Location: Mapped[Optional[str]] = mapped_column(String)
    time_open: Mapped[int] = mapped_column(SmallInteger)
    time_closed: Mapped[int] = mapped_column(SmallInteger)
    provider: Mapped["Provider"] = relationship(back_populates="canteens")
    sqlite_autoincrement = True

    def __repr__(self) -> str:
        """Canteen class string representation."""
        return f"ID: {self.ID}\nProvideID: {self.ProviderID}\nName: {self.Name}\nLocation: \
            {self.Location}\ntime_open: {self.time_open}\ntime_closed: {self.time_closed}\n"


if __name__ == "__main__":
    Canteen.__table__.drop(engine, checkfirst=True)
    Provider.__table__.drop(engine, checkfirst=True)
    # Base.metadata.drop_all(engine, checkfirst=True)
    Provider.__table__.create(engine, checkfirst=True)
    Canteen.__table__.create(engine, checkfirst=True)
    # Base.metadata.create_all(engine, checkfirst=True)
