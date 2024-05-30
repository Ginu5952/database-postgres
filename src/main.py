
from src.db import fetch_all,fetch_by_id,ROW_DATA_TYPE,insert_data,fetch_highly_paid_employee,count_by_gender,update_data,update_column_name,delete_row_by_id

def main():
    # Fetch all employees
    employees:list[ROW_DATA_TYPE] = fetch_all()
    print(employees)

    highly_paid_employees = fetch_highly_paid_employee(1)
    print("\nHighly paid employees:", highly_paid_employees)

    gender = 'M'
    count = count_by_gender(gender)
    print(f"\nNumber of employees with gender {gender}: {count}")

    employee_id = int(input('\nENTER an id: '))
    employee = fetch_by_id(employee_id)
    print(employee)

    # insert r-required o-optional
    data = []
    for field, state in [
        ("first_name", "r"),
        ("last_name", "o"),
        ("email","r"),
        ("gender","o"),
        ("salary","o")
    ]:
        input_data = input(f"{field} {'{Default None}' if state == 'o' else ''}")
        if len(input_data) == 0 and state == 'o':
            input_data = None
        data.append(input_data)   

    result = insert_data(data)
    print(result)   
    output = update_values()
    update_data(output)

    
    old, new = get_columns_to_update()
    update_column_name(old,new)
    
    id = delete_row()
    delete_row_by_id(id)
   

def update_values() -> list:
     
    updated_data = []
    print("Enter the data to be update\n")

    for value, state in [
        ("serial_id","r"),
        ("first_name", "r"),
        ("last_name", "o"),
        ("email","r"),
        ("gender","o"),
        ("salary","o")
    ]:

        updatee_data = input(f"{value} {'{Default None}' if state == 'o' else ''}")
        if len(updatee_data) == 0 and state == 'o':
            updatee_data = None
        updated_data.append(updatee_data) 
        
    return updated_data

def get_columns_to_update() -> tuple[str, str]:

    while True:
       
        input_data = input('\nEnter column name and new column name to be updated, separated by a comma: ')
        
        parts = input_data.split(',')
        
        if len(parts) == 2:
            old_clm_name = parts[0].strip()
            new_clm_name = parts[1].strip()
            
          
            if old_clm_name and new_clm_name:
                return old_clm_name, new_clm_name
      
        print("Invalid input. Please enter both column names separated by a comma.")



def create_new_csv():

    import csv

    with open('/home/dci-student/Downloads/MOCK_DATA.csv','r') as source:
        source_reader = csv.reader(source)
        with open('/home/dci-student/Downloads/MOCK_DATA_copy.csv','w') as dest:
            dest_writer = csv.writer(dest)
            for row in source_reader:
                new_row = row[1:]
                dest_writer.writerow(new_row)

def delete_row() -> int:
    try:
        id = int(input('\nEnter the id of the row to delete: '))
        return id
    except ValueError:
        print("Invalid input. Please enter a valid integer.")
        return delete_row()


if __name__ == '__main__':
    main()    
   #create_new_csv()