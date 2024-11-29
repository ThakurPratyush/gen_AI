import sqlite3
## db exsists by default in python3

connection = sqlite3.connect("student.db")

cursor = connection.cursor()

table_info = """
create table stream(NAME VARCHAR(20), 
id INT
)
"""
cursor.execute(table_info)

## Insert some more records
cursor.execute('''Insert Into stream values('Data Science','1001')''')
cursor.execute('''Insert Into stream values('DEVOPS','1002')''')

## DISPLAY ALL RECORDS
print("inserted recs are :")
data = cursor.execute('''
                      select * from stream''')

## data in form of list 
for row in data:
    print(row)
    
## Commit your changes in the database
connection.commit()
connection.close()