# Databases and Python

This program contains example code for `SQL` queries using `Python` and `SQLite3`.<br>
The same functionality is provided with plain SQL queries as well as using `SQLAlchemy` ORM.<br>
This program is created as a part of [Advanced Python](https://ois.ttu.ee/portal/page?_pageid=37,674581&_dad=portal&_schema=PORTAL&link=D7EB473292336F86) course at [Tallinn University of Technology](https://taltech.ee/) instructed by Einar Kivisalu.<br>

## Assignment description
Here are 8 diners[^1] in different buildings of TalTech:<br>

|  | Location	| Service provider | Open |
|:--- |:---|:---|:---|
| Economics- and social science building canteen | Akadeemia tee 3 SOC- building | Rahva Toit |	8.30-18.30 |
| Library canteen | Akadeemia tee 1/Ehitajate tee 7 | Rahva Toit |	8.30-19.00 |
| Main building Deli cafe | Ehitajate tee 5 U01 building | Baltic Restaurants Estonia AS |	9.00-16.30 |
| Main building Daily lunch restaurant | Ehitajate tee 5 U01 building | Baltic Restaurants Estonia AS |	9.00-16.30 |
| U06 building canteen |  | Rahva toit | 9.00-16.00 |
| Natural Science building canteen | Akadeemia tee 15 SCI building | Baltic Restaurants Estonia AS | 9.00-16.00 |		
| ICT building canteen | Raja 15/Mäepealse 1 | Baltic Restaurants Estonia AS | 9.00-16.00 |
| Sports building canteen | Männiliiva 7 S01 building | TTÜ Sport OÜ | 11.00-20.00 |

and IT College diner:<br>
<br>
|  | Location	| Service provider | Open |
|:--- |:---|:---|:---|
| bitStop KOHVIK | IT College, Raja 4c | Bitt OÜ | 9.30-16.00 |

[^1]: Data from old TalTech homepage and actual opening times may have been changed. <br>

There are 4 service providers in total:<br>
+ Rahva Toit, 
+ Baltic Restaurants Estonia AS, 
+ TTÜ Sport and 
+ Bitstop Kohvik OÜ.

There are different opening hours for every canteen.<br>

Task:
A. Use Python wrapped plain SQL language

1. Create SQLite database `DINERS`, with two related tables `CANTEEN` and `PROVIDER`<br>

Table `CANTEEN` fields: `ID`, `ProviderID`, `Name`, `Location`, `time_open`, `time_closed` (weekday doesn't matter).<br>
Table `Provider` fields: `ID`, `ProviderName`.<br>
<br>
If you want, you may add some additional fields, but not necessary.<br>

2. Insert IT College canteen data by separate statement, other canteens as one list.

3. Create query for canteens which are open 09.00-16.20 (full period).

4. Create query for canteens which are serviced by `Baltic Restaurants Estonia AS`.<br>
NB! Create query by string `"Baltic Restaurants Estonia AS"` not by direct ID!.<br>

B. Use `SqlAlchemy` or any other ORM and solve p 1-4 again! Please create different database.<br>

Additional Information:<br>
+ Tests and `GUI` are not necessary.
+ Add documentation and comments.

Hints:<br>
+ `SQLite` datatypes: https://www.sqlite.org/datatype3.html
+ How to join and query data from related tables using `SQLAlchemy`: https://community.snowflake.com/s/article/How-to-Join-2-tables-using-SQL-Alchemy


## Running the application
To run this program

### Solution using plain SQL

[sql_connect.py](address)

### Solution using `SQLAlchemy`

[sqlAlchemyEngine.py](address)