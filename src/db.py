import psycopg as pg
from decimal import Decimal


ROW_DATA_TYPE = tuple[int, str, str, str, str, Decimal]
INSERT_DATA_TYPE = tuple[str, str, str, str, int]

CONN = pg.connect(
    user='postgres',
    password='postgres',
    dbname='dci'
)

# TODO: SELECT
def fetch_all() -> list[ROW_DATA_TYPE]:
    """Fetch All employees"""
    # query
    query = """
        SELECT * 
        FROM company.employee;
    """

    # cursor
    with CONN.cursor() as cursor:
        cursor.execute(query)
        employees = cursor.fetchall()
        return employees

def fetch_by_id(employee_id: int) -> ROW_DATA_TYPE | None:
    """Fetch by id"""
    query = """
        SELECT * 
        FROM company.employee
        WHERE serial_id = %s;
    """

    with CONN.cursor() as cursor:
        cursor.execute(query, [employee_id])
        employee = cursor.fetchone()
        return employee

def fetch_highly_paid_employee(limit: int) -> list[ROW_DATA_TYPE]:

    query = """
        SELECT * 
        FROM company.employee
        WHERE salary = (SELECT MAX(salary) FROM company.employee)
        LIMIT %s;
    """
    with CONN.cursor() as cursor:
        cursor.execute(query, [limit])
        employees = cursor.fetchall()
        return employees

def count_by_gender(gender: str) -> int:

    """Count employees by gender"""
    query = """
        SELECT COUNT(*)
        FROM company.employee
        WHERE gender = %s;
    """
    with CONN.cursor() as cursor:
        cursor.execute(query, [gender])
        count = cursor.fetchone()[0] # [0] accesses the first element (column) of the tuple returned by fetchone()
        return count

# TODO: Analyse the data and extract more information for learning purposes

# TODO: INSERT
def insert_data(data: INSERT_DATA_TYPE) -> ROW_DATA_TYPE:
    query = """
        INSERT INTO company.employee
        VALUES (DEFAULT, %s, %s, %s, %s, %s)
        RETURNING *;
    """

    with CONN.cursor() as cursor:
        cursor.execute(query, data) # data should be an iterable.
        employee = cursor.fetchone()
        # Any action that modifies the database needs to be committed.
        CONN.commit()
        return employee


# TODO: UPDATE
def update_data(data:ROW_DATA_TYPE) -> ROW_DATA_TYPE:
    query = """
        UPDATE company.employee
        SET first_name = %s,
            last_name = %s,
            email = %s,
            gender = %s,
            salary = %s
        WHERE serial_id = %s
        RETURNING *;
    """
    with CONN.cursor() as cursor:
            employee_id = data[0]
            cursor.execute(query, (*data[1:], employee_id))
            updated_employee = cursor.fetchone()
            CONN.commit()
            print(f"Employee with ID {employee_id} updated successfully.")
            return updated_employee
    
def update_column_name(old_column_name, new_column_name):

    query = f"""
        ALTER TABLE company.employee
        RENAME COLUMN {old_column_name} TO {new_column_name};
    """
    with CONN.cursor() as cursor:
        cursor.execute(query)
        print(f'The column {old_column_name} is renamed to {new_column_name} successfully')
        CONN.commit()
    
def delete_row_by_id(id:int):

    with CONN.cursor() as cursor:
            # Check if the ID exists
            cursor.execute("SELECT 1 FROM company.employee WHERE serial_id = %s", (id,))
            if cursor.fetchone():
                # ID exists, proceed with deletion
                cursor.execute("DELETE FROM company.employee WHERE serial_id = = %s", (id,))
                CONN.commit()
                print(f"Row with id {id} has been deleted.")
            else:
                # ID does not exist
                print(f"No row found with id {id}.")



