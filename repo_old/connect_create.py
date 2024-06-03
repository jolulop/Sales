import pyodbc

def create_connection(server, database, username, password):
    connection = None
    try:
        connection = pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};'
            f'SERVER={server};'
            f'DATABASE={database};'
            f'UID={username};'
            f'PWD={password}'
        )
        print("Connection to SQL Server successful")
    except pyodbc.Error as e:
        print(f"The error '{e}' occurred")
    return connection

def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query executed successfully")
    except pyodbc.Error as e:
        print(f"The error '{e}' occurred")

def execute_read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except pyodbc.Error as e:
        print(f"The error '{e}' occurred")

# Connection details
server = "timia.database.windows.net"
database = "sales"
username = "CloudSA85ee9ad0"
password = "!nDXg4Q#JqNs8bCK"

# Connect to the database
connection = create_connection(server, database, username, password)



# Example: Create a table
alter_table_query = """ALTER TABLE RESPONSABLE ADD CONSTRAINT FK_RESPONSABLE_PERSON_ID FOREIGN KEY (person_id) REFERENCES PERSONAS(id);"""
execute_query(connection, alter_table_query)

# Example: Insert data
# insert_employee_query = """INSERT INTO employees (name, age) VALUES ('John Doe', 28), ('Jane Smith', 34)"""
# execute_query(connection, insert_employee_query)

# # Example: Retrieve data
# select_employees_query = "SELECT * FROM employees"
# employees = execute_read_query(connection, select_employees_query)

# for employee in employees:
#     print(employee)    