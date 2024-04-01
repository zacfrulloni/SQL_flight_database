import sqlite3
from sqlite3 import Error
import time

def make_connection(database_file):
    """ Create a connection to the database file.
    Variables:
    database_file (str): name of db file.

    Returns:
    connection: connection to the database"""
    connection = None
    try:
        connection = sqlite3.connect(database_file)
        print(f"Successfully connected to {database_file}")
    except Error as e:
        print(e)
    return connection

def make_query(connection, query):
    """ Executes queries to SQL tables.

    Variables:
    connection: connection to the database
    query: The SQL query that will be executed

    Returns:
    result: the result of the query """
    try:
        cursor = connection.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        connection.commit()
        return result
    except Error as e:
        print(e)

def list_all_tables(connection):
    """ Lists all the tables in the database.

    Variables:
    connection: connection to the database

    Returns:
    list_of_tables: names of tables.
    """
    query = "SELECT name FROM sqlite_master WHERE type ='table';"
    list_of_tables=[]
    try:
        cursor = connection.cursor()
        cursor.execute(query)
        tables = cursor.fetchall()
        if tables:
            list_of_tables = [table[0] for table in tables]
            return list_of_tables
        else:
            print("Database is empty.")
    except Error as e:
        print(e)

def view_table_data(connection, table_name):
    """ gets all the data for a specific table.

    Variables:
    connection: connection to the database
    table_name: The name of a specific table """
    cursor = connection.cursor()
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = cursor.fetchall()
    column_names = [column[1] for column in columns]

    # get and print data
    query = f"SELECT * FROM {table_name};"
    table_data = make_query(connection, query)

    if column_names and table_data:
        # Print the column names
        print(", ".join(column_names))
        
        # Print data
        for row in table_data:
            print(", ".join(map(str, row)))
    else:
        print(f"{table_name} table has no data.")
    return None

# Database file
database_file = "aircraft_management_system_db.db"

# Create a connection to the database
connection = make_connection(database_file)

# Drop tables on initialisation
# tables_to_drop = ["Aircraft", "Flight", "Pilot", "Destination", "Pilot_Flight", "Aircraft_Destination", "Aircraft_Flight"]

# for table in tables_to_drop:
#     table_drop = f"DROP TABLE IF EXISTS {table};"
#     make_query(connection, table_drop)

# Create tables
aircraft_table = """ CREATE TABLE IF NOT EXISTS Aircraft (
    Aircraft_Registration_Number VARCHAR(25) PRIMARY KEY,
    Seat_Capacity INT,
    Manufacturer VARCHAR(25) NOT NULL,
    Status TEXT CHECK (Status IN ('Active', 'Maintenance', 'Retired')) NOT NULL); """

flight_table = """ CREATE TABLE IF NOT EXISTS Flight (
    Flight_Number VARCHAR (25) PRIMARY KEY,
    Aircraft_Registration_Number VARCHAR(25) REFERENCES Aircraft(Aircraft_Registration_Number) NOT NULL,
    Departure_Airport_Code VARCHAR(25) NOT NULL,
    Arrival_Airport_Code VARCHAR(25) NOT NULL,
    Departure_Date_Time DATETIME,
    Arrival_Date_Time DATETIME,
    Passenger_Count INT,
    Flight_Duration INT ); """

pilot_table = """ CREATE TABLE IF NOT EXISTS Pilot (
    Commercial_Pilot_License_Number VARCHAR(25) PRIMARY KEY,
    First_Name VARCHAR(25) NOT NULL,
    Last_Name VARCHAR(25) NOT NULL,
    License_Number VARCHAR(25) NOT NULL,
    Contact_Number VARCHAR(25) NOT NULL,
    Pilot_Ranking TEXT CHECK (Pilot_Ranking IN ('Cadet', 'Captain')) NOT NULL ); """

destination_table = """ CREATE TABLE IF NOT EXISTS Destination (
    Airport_Destination_Code VARCHAR(25) PRIMARY KEY,
    Location VARCHAR(25) NOT NULL,
    Country VARCHAR(25) NOT NULL ); """

pilot_flight_table = """ CREATE TABLE IF NOT EXISTS Pilot_Flight (
    Pilot_Flight_ID INT PRIMARY KEY,
    Commercial_Pilot_License_Number VARCHAR(25) REFERENCES Pilot(Commercial_Pilot_License_Number),
    Flight_Number VARCHAR (25) REFERENCES Flight(Flight_Number),
    Pilot_Ranking TEXT CHECK (Pilot_Ranking IN ('Pilot Cadet', 'Second officer', 'Cadet', 'Captain')) NOT NULL ); """

aircraft_destination_table = """ CREATE TABLE IF NOT EXISTS Aircraft_Destination (
    Aircraft_Destination_ID INT PRIMARY KEY,
    Aircraft_Registration_Number VARCHAR(25) REFERENCES Aircraft(Aircraft_Registration_Number),
    Airport_Destination_Code VARCHAR(25) REFERENCES Destination(Airport_Destination_Code) ); """

aircraft_flight_table = """ CREATE TABLE IF NOT EXISTS Aircraft_Flight (
    Aircraft_Flight_ID INT PRIMARY KEY,
    Aircraft_Registration_Number VARCHAR(25) REFERENCES Aircraft(Aircraft_Registration_Number),
    Flight_Number VARCHAR (25) REFERENCES Flight(Flight_Number) ); """

tables_to_create = [aircraft_table, flight_table, pilot_table,
    destination_table, pilot_flight_table, aircraft_destination_table, aircraft_flight_table]

# create queries
for table_query in tables_to_create:
    make_query(connection, table_query)

# Insert data into sql tables
aircraft_data = """ INSERT INTO Aircraft (Aircraft_Registration_Number, Seat_Capacity, Manufacturer, Status)
VALUES
  ('EI-DCJ', 150, 'Boeing', 'Active'),
  ('F-WWBY', 200, 'Airbus', 'Active'),
  ('EI-HGA', 100, 'Ryanair', 'Active'),
  ('EI-DAJ', 180, 'Boeing', 'Maintenance'),
  ('F-WWAY', 250, 'Airbus', 'Retired'); """

flight_data = """ INSERT INTO Flight (Flight_Number, Aircraft_Registration_Number, Departure_Airport_Code, Arrival_Airport_Code, Departure_Date_Time, Arrival_Date_Time, Passenger_Count, Flight_Duration)
VALUES
  ('B777', 'EI-DCJ', 'STD', 'EDI', '2023-10-30 08:00:00', '2023-10-30 09:30:00', 122, 1.5),
  ('F56', 'F-WWBY', 'BRI', 'MXP', '2023-11-01 14:30:00', '2023-11-01 16:30:00', 171, 2),
  ('FR2233', 'EI-HGA', 'MAD', 'BUD', '2023-11-05 10:45:00', '2023-11-05 16:45:00', 80, 3.5),
  ('B677', 'EI-DAJ', 'LIS', 'PRA', '2023-11-10 12:30:00', '2023-11-10 18:30:00', 169, 3),
  ('112', 'F-WWAY', 'BER', 'FCO', '2023-11-15 09:15:00', '2023-11-15 11:15:00', 201, 2); """

pilot_data = """ INSERT INTO Pilot (Commercial_Pilot_License_Number, First_Name, Last_Name, License_Number, Contact_Number, Pilot_Ranking)
VALUES
  ('CPL001', 'John', 'Wayne', 'L12345', '07704144166', 'Captain'),
  ('CPL002', 'Robin', 'Gray', 'L67890', '08804188111', 'Cadet'),
  ('CPL003', 'Felix', 'Arthur', 'L54321', '02804128121', 'Captain'),
  ('CPL004', 'James', 'Williams', 'L99999', '3304195111', 'Cadet'),
  ('CPL005', 'Ben', 'Simpson', 'L11111', '55804143111', 'Captain'),
  ('CPL006', 'Larry', 'Wilks', 'L12345', '77804188111', 'Cadet'),
  ('CPL007', 'Marc', 'Stewart', 'L67890', '09904188111', 'Captain'),
  ('CPL008', 'Shaun', 'Proctor', 'L54321', '11114188111', 'Cadet'),
  ('CPL009', 'Ben', 'Aaron', 'L99999', '22224188111', 'Captain'),
  ('CPL010', 'Marc', 'Leith', 'L11111', '333341881112', 'Cadet'); """

destination_data = """ INSERT INTO Destination (Airport_Destination_Code, Location, Country)
VALUES
  ('EDI', 'Edinburgh', 'UK'),
  ('MXP', 'Milan', 'Italy'),
  ('BUD', 'Budapest', 'Hungary'),
  ('PRG', 'Prague', 'Czech Republic'),
  ('FCO', 'Rome', 'Italy'); """

pilot_flight_data = """ INSERT INTO Pilot_Flight (Pilot_Flight_ID, Commercial_Pilot_License_Number, Flight_Number, Pilot_Ranking)
VALUES
  (1, 'CPL001', 'B777', 'Captain'),
  (2, 'CPL002', 'B777', 'Cadet'),
  (3, 'CPL003', 'F56', 'Captain'),
  (4, 'CPL004', 'F56', 'Cadet'),
  (5, 'CPL005', 'FR2233', 'Captain'),
  (6, 'CPL006', 'FR2233', 'Cadet'),
  (7, 'CPL007', 'B677', 'Captain'),
  (8, 'CPL008', 'B677', 'Cadet'),
  (9, 'CPL09', '112', 'Captain'),
  (10, 'CPL010', '112', 'Cadet'); """

aircraft_destination_data = """ INSERT INTO Aircraft_Destination (Aircraft_Destination_ID, Aircraft_Registration_Number, Airport_Destination_Code)
VALUES
  (1, 'EI-DCJ', 'EDI'),
  (2, 'F-WWBY', 'MXP'),
  (3, 'EI-HGA', 'BUD'),
  (4, 'EI-DAJ', 'PRG'),
  (5, 'F-WWAY', 'FCO'); """

aircraft_flight_data = """ INSERT INTO Aircraft_Flight (Aircraft_Flight_ID, Aircraft_Registration_Number, Flight_Number)
VALUES
  (1, 'EI-DCJ', 'B777'),
  (2, 'F-WWBY', 'F56'),
  (3, 'EI-HGA', 'FR2233'),
  (4, 'EI-DAJ', 'B677'),
  (5, 'F-WWAY', '112'); """

insert_data = [aircraft_data, flight_data, pilot_data,
    destination_data, pilot_flight_data, aircraft_destination_data, aircraft_flight_data]

# create tables
for insert_query in insert_data:
    make_query(connection, insert_query)

# start menu:
while True:
    print("\n\nSTART MENU\n")
    print("1. List all tables")
    print("2. View table data")
    print("3. Search data")
    print("4. Update data")
    print("5. Delete data")
    print("6. Insert data")
    print("7. Get the length of an entire flight and total passenger count")
    print("8. Find available aircrafts")
    print("9. Find pilots by rank")
    print("10. Quit\n")
    
    choice = input("Select one of the following (1-10): ")    
    if choice == '1':
        print("\n===========LIST OF TABLES===========\n")
        # when the user uses a specific table store variable table_name to execute commands
        while True:
            tables=list_all_tables(connection)
            list_tables=[]
            count=0
            for table in tables:
                count=count+1
                list_tables.append(f"{count}. {table}")
            for table in list_tables:
                print(table)
            time.sleep(2)
            break
        
    elif choice == '2':
        # SELECT A SPECIFIC TABLE
        tables=list_all_tables(connection)
        list_tables=[]
        count=0
        for table in tables:
            count=count+1
            list_tables.append(f"{count}. {table}")
        for table in list_tables:
            print(table)
        choice = input(f"\nNow select one of the {count} tables by typing the number of the desired table or type 'x' to go back to the start menu: \n")
        if choice.isdigit() and 1 <= int(choice) <= 100:
            table_name = tables[int(choice) - 1]
            view_table_data(connection, table_name)
            time.sleep(2)
            continue
        elif choice =='x':
            time.sleep(2)
            continue
        elif (choice.lower() == 'x' or (choice.isdigit() and 1 <= int(choice) <= count) is not True):
            print(f"Invalid choice. Please enter a number between 1 and {count}.")
            time.sleep(2)
            continue
        else:
            time.sleep(2)
            break
    elif choice=='3':
        query="SELECT name FROM sqlite_master WHERE type='table';"
        cursor = connection.cursor()
        cursor=cursor.execute(query)
        table_names = cursor.fetchall()
        attribute_value=input('input the attribute you are searching for (case sensitive): ')
        for table in table_names:
            table_name = table[0]

            column_names_query = f"PRAGMA table_info({table_name});"
            cursor.execute(column_names_query)
            columns = cursor.fetchall()
            column_names = [column[1] for column in columns]

            select_query = f"SELECT * FROM {table_name} WHERE {f'=? OR '.join(column_names)}=?;"
            cursor.execute(select_query, [attribute_value]*len(column_names))
            records = cursor.fetchall()

            # Print the results
            if records:
                print(f"\n Matching records in table {table_name}:")
                for record in records:
                    print(record)
            else:
                print(f"No matching records were found in table {table_name}")
            time.sleep(2)
    elif choice == '4':
        # SELECT A SPECIFIC TABLE
        tables=list_all_tables(connection)
        list_tables=[]
        count=0
        for table in tables:
            count=count+1
            list_tables.append(f"{count}. {table}")
        for table in list_tables:
            print(table)
        choice = input(f"\nNow select one of the {count} tables by typing the number of the desired table or type 'x' to go back to the start menu: \n")
        print('\n')
        if choice.isdigit() and 1 <= int(choice) <= 100:
            table_name = tables[int(choice) - 1]
            cursor = connection.cursor()
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = cursor.fetchall()
            column_names = [column[1] for column in columns]
            count=0
            column_list=[]
            for col in column_names:
                count=count+1
                column_list.append(f"{count}. {col}")
            for col in column_list:
                print(col)
            column_count=len(column_names)
            choice = input(f"\nNow select one of the {column_count} columns from the {table_name} table or type 'x' to go back to the start menu: \n")
            print('\n')
            if choice.isdigit() and 1 <= int(choice) <= 100:
                col_name = column_names[int(choice) - 1]
                query = f"SELECT {col_name} FROM {table_name};"
                cursor = connection.cursor()
                cursor=cursor.execute(query)
                rows = cursor.fetchall()
                row_names = [row[0] for row in rows]
                count=0
                row_list=[]
                for row in row_names:
                    count=count+1
                    row_list.append(f"{count}. {row}")
                for row in row_list:
                    print(row)
                row_count=len(row_list)
                choice = input(f"\nNow select one of the {row_count} rows from the {table_name} table or type 'x' to go back to the start menu: \n")
                print('\n')
                if choice.isdigit() and 1 <= int(choice) <= 100:
                    new_value=input("Type in the updated value:")
                    row_value = row_names[int(choice) - 1]
                    query = f"UPDATE {table_name} SET {col_name} = '{new_value}' WHERE {col_name} = '{row_value}';"
                    cursor = connection.cursor()
                    cursor=cursor.execute(query)
                    print('\nUPDATED TABLE:\n')
                    view_table_data(connection, table_name)
                    time.sleep(2)
                elif choice =='x':
                    time.sleep(2)
                    continue
                elif (choice.lower() == 'x' or (choice.isdigit() and 1 <= int(choice) <= count) is not True):
                    print(f"Invalid choice. Please enter a number between 1 and {count}.")
                    time.sleep(2)
                    continue
                else:
                    time.sleep(2)
                    break
            elif (choice.lower() == 'x' or (choice.isdigit() and 1 <= int(choice) <= count) is not True):
                print(f"Invalid choice. Please enter a number between 1 and {count}.")
                time.sleep(2)
                continue
            else:
                time.sleep(2)
                break
        elif choice =='x':
            time.sleep(2)
            continue
        elif (choice.lower() == 'x' or (choice.isdigit() and 1 <= int(choice) <= count) is not True):
            print(f"Invalid choice. Please enter a number between 1 and {count}.")
            time.sleep(2)
            continue
        else:
            time.sleep(2)
            break
    elif choice == '5':
        # SELECT A SPECIFIC TABLE
        tables=list_all_tables(connection)
        list_tables=[]
        count=0
        for table in tables:
            count=count+1
            list_tables.append(f"{count}. {table}")
        for table in list_tables:
            print(table)
        choice = input(f"\nNow select one of the {count} tables by typing the number of the desired table or type 'x' to go back to the start menu: \n")
        if choice.isdigit() and 1 <= int(choice) <= 100:
            table_name = tables[int(choice) - 1]
            table=view_table_data(connection, table_name)
            choice = input(f"\nType '1' to delete a column or '2' to delete a row: \n")
            if choice=='1':
                # delete column
                column = input(f"\nType in the column you want to delete (case sensitive): \n")
                query = f"ALTER TABLE {table_name} DROP {column};"
                cursor = connection.cursor()
                cursor=cursor.execute(query)
                print('\nUPDATED TABLE:\n')
                view_table_data(connection, table_name)
                time.sleep(2)
            elif choice=='2':
                # delete row
                col = input(f"\nType in the value of the column of the row you want to delete (case sensitive): \n")
                row = input(f"\nType in the value of the row you want to delete (case sensitive): \n")
                query = f"DELETE FROM {table_name} WHERE {col} = '{row}';"
                cursor = connection.cursor()
                cursor=cursor.execute(query)
                print('\nUPDATED TABLE:\n')
                view_table_data(connection, table_name)
                time.sleep(2)
            elif choice =='x':
                time.sleep(2)
                continue
            else:
                print(f"Invalid input, please try again.")
                time.sleep(2)
    elif choice == '6':
        # SELECT A SPECIFIC TABLE
        tables=list_all_tables(connection)
        list_tables=[]
        count=0
        for table in tables:
            count=count+1
            list_tables.append(f"{count}. {table}")
        for table in list_tables:
            print(table)
        choice = input(f"\nNow select one of the {count} tables by typing the number of the desired table or type 'x' to go back to the start menu: \n")
        if choice.isdigit() and 1 <= int(choice) <= 100:
            table_name = tables[int(choice) - 1]
            print('Selected table:')
            table=view_table_data(connection, table_name)
            table_name = tables[int(choice) - 1]
            cursor = connection.cursor()
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = cursor.fetchall()
            column_names = [column[1] for column in columns]
            col_tuple = tuple(item.replace("'", "") for item in column_names)
            values=[]
            print('\nfor each column insert value\n')
            for col in column_names:
                choice=input(f'{col}:')
                values.append(choice)
            values=tuple(values)
            query = f"INSERT INTO {table_name} {col_tuple} VALUES {values};"
            cursor = connection.cursor()
            cursor=cursor.execute(query)
            print('\nUPDATED TABLE:\n')
            view_table_data(connection, table_name)
            time.sleep(2)
        elif choice =='x':
            time.sleep(2)
            continue
        else:
            print(f"Invalid input, please try again.")
            time.sleep(2)
    elif choice == '7':
        table_name="Flight"
        query = f"SELECT Flight_Number FROM Flight;"
        cursor = connection.cursor()
        flight_n=cursor.execute(query)
        flight_numbers = [row[0] for row in flight_n]
        count=0
        flight_numbers_list=[]
        for f_n in flight_numbers:
            count=count+1
            flight_numbers_list.append(f"{count}. {f_n}")
        for f_n in flight_numbers_list:
            print(f_n)
        choice = input(f"\nNow type in the number of the desired flight number (1-n) to get flight duration and passenger count or type 'x' to go back to the start menu: \n")
        if choice.isdigit() and 1 <= int(choice) <= 100:
            f_n = flight_numbers[int(choice) - 1]
            query = f"SELECT Flight_Duration, Passenger_Count FROM Flight WHERE Flight_Number='{f_n}';"
            # SELECT column1, column2 FROM table1, table2 WHERE column2='value';
            cursor = connection.cursor()
            result=cursor.execute(query)
            for values in result:
                print(f'Total flight duration: {values[0]}\nTotal passenger count: {values[1]} ')
            time.sleep(2)
        elif choice =='x':
            time.sleep(2)
            continue
        else:
            print(f"Invalid input, please try again.")
            time.sleep(2)
    elif choice =='8':
        choice = input(f"\n Search one of the following (1-3) \n 1. active \n 2. retired \n 3. in maintenance \n or type 'x' to go back to the start menu: \n")
        if choice=='1':
            query = f"SELECT Aircraft_Registration_Number, manufacturer FROM Aircraft WHERE Status='Active';"
            cursor = connection.cursor()
            result=cursor.execute(query)
            for r in result:
                print(r[0])
            time.sleep(2)
        elif choice =='2':
            query = f"SELECT Aircraft_Registration_Number, manufacturer FROM Aircraft WHERE Status='Retired';"
            cursor = connection.cursor()
            result=cursor.execute(query)
            for r in result:
                print(r[0])
            time.sleep(2)
        elif choice =='3':
            query = f"SELECT Aircraft_Registration_Number, manufacturer FROM Aircraft WHERE Status='Maintenance';"
            cursor = connection.cursor()
            result=cursor.execute(query)
            for r in result:
                print(r[0])
            time.sleep(2)
        elif choice =='x':
            time.sleep(2)
            continue
        else:
            print(f"Invalid input, please try again.")
            time.sleep(2)
    elif choice =='9':
        choice = input(f"\n Search one of the following (1-2) \n 1. Captain \n 2. Cadet \n or type 'x' to go back to the start menu: \n")
        if choice =='1':
            query = f"SELECT First_Name, Last_Name FROM Pilot WHERE Pilot_Ranking='Captain';"
            cursor = connection.cursor()
            result=cursor.execute(query)
            for r in result:
                print(r[0])
            time.sleep(2)
        elif choice =='2':
            query = f"SELECT First_Name, Last_Name FROM Pilot WHERE Pilot_Ranking='Cadet';"
            cursor = connection.cursor()
            result=cursor.execute(query)
            for r in result:
                print(r[0])
            time.sleep(2)
        elif choice =='x':
            time.sleep(2)
            continue
        else:
            print(f"Invalid input, please try again.")
            time.sleep(2)
    elif choice =='10':
        time.sleep(2)
        break
    else:
        print("Invalid choice. Please enter a number between 1 and 10.")
        time.sleep(2)

# Close the connection
if connection:
    connection.close()
    print("Connection closed")