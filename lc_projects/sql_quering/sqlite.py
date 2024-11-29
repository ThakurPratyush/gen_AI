import sqlite3
## db exsists by default in python3

connection = sqlite3.connect("student.db")

cursor = connection.cursor()

table_info = """
create table STUDENT(NAME VARCHAR(20), 
CLASS VARCHAR(25),SECTION VARCHAR(20),MARKS INT
)
"""
cursor.execute(table_info)

## Insert some more records
cursor.execute('''Insert Into STUDENT values('ABC','Data Science','A',90)''')
cursor.execute('''Insert Into STUDENT values('DEP','Data Science','B',100)''')
cursor.execute('''Insert Into STUDENT values('IKL','Data Science','A',86)''')
cursor.execute('''Insert Into STUDENT values('JDK','DEVOPS','A',50)''')
cursor.execute('''Insert Into STUDENT values('YEH','DEVOPS','A',35)''')

## DISPLAY ALL RECORDS
print("inserted recs are :")
data = cursor.execute('''
                      select * from student''')

## data in form of list 
for row in data:
    print(row)
    
## Commit your changes in the database
connection.commit()
connection.close()