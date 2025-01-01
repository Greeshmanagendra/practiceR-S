
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

# Create an engine and a base class
engine = create_engine('sqlite:///corporate_employee.db', echo=True)
Base = declarative_base()

# Define the Corporate table
class Corporate(Base):
    __tablename__ = 'corporates'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    location = Column(String)

# Define the Employee table
class Employee(Base):
    __tablename__ = 'employees'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)
    corporate_id = Column(Integer, ForeignKey('corporates.id'))
    corporate = relationship("Corporate", back_populates="employees")

Corporate.employees = relationship("Employee", order_by=Employee.id, back_populates="corporate")

# Create the tables
Base.metadata.create_all(engine)

# Create a session
Session = sessionmaker(bind=engine)
session = Session()

# Function to insert data
def insert_corporate(name, location):
    try:
        new_corporate = Corporate(name=name, location=location)
        session.add(new_corporate)
        session.commit()
        print("Corporate added successfully")
    except Exception as e:
        session.rollback()
        print(f"Error: {e}")

def insert_employee(name, age, corporate_id):
    try:
        new_employee = Employee(name=name, age=age, corporate_id=corporate_id)
        session.add(new_employee)
        session.commit()
        print("Employee added successfully")
    except Exception as e:
        session.rollback()
        print(f"Error: {e}")

# Function to delete data
def delete_corporate(corporate_id):
    try:
        corporate = session.query(Corporate).filter(Corporate.id == corporate_id).one()
        session.delete(corporate)
        session.commit()
        print("Corporate deleted successfully")
    except Exception as e:
        session.rollback()
        print(f"Error: {e}")

def delete_employee(employee_id):
    try:
        employee = session.query(Employee).filter(Employee.id == employee_id).one()
        session.delete(employee)
        session.commit()
        print("Employee deleted successfully")
    except Exception as e:
        session.rollback()
        print(f"Error: {e}")

# Function to update data
def update_corporate(corporate_id, name=None, location=None):
    try:
        corporate = session.query(Corporate).filter(Corporate.id == corporate_id).one()
        if name:
            corporate.name = name
        if location:
            corporate.location = location
        session.commit()
        print("Corporate updated successfully")
    except Exception as e:
        session.rollback()
        print(f"Error: {e}")

def update_employee(employee_id, name=None, age=None, corporate_id=None):
    try:
        employee = session.query(Employee).filter(Employee.id == employee_id).one()
        if name:
            employee.name = name
        if age:
            employee.age = age
        if corporate_id:
            employee.corporate_id = corporate_id
        session.commit()
        print("Employee updated successfully")
    except Exception as e:
        session.rollback()
        print(f"Error: {e}")

# Insert sample data
insert_corporate('TechCorp', 'New York')
insert_corporate('HealthInc', 'San Francisco')
insert_corporate('FinTech','India')
insert_employee('A', 35, 1)
insert_employee('B', 20, 2)
insert_employee('C',20, 3)

# Perform join, order by, group by, and filter operations
def query_operations():
    try:
        # Join
        results = session.query(Corporate, Employee).join(Employee, Corporate.id == Employee.corporate_id).all()
        for corporate, employee in results:
            print(f"Corporate: {corporate.name}, Employee: {employee.name}")

        # Order by
        ordered_employees = session.query(Employee).order_by(Employee.age).all()
        for employee in ordered_employees:
            print(f"Ordered Employee: {employee.name}, Age: {employee.age}")

        # Group by and filter
        grouped_employees = session.query(Employee.age, func.count(Employee.id)).group_by(Employee.age).having(func.count(Employee.id) > 1).all()
        for age, count in grouped_employees:
            print(f"Age: {age}, Count: {count}")
    except Exception as e:
        print(f"Error: {e}")


update_employee(2, name='R', age=26)

delete_corporate(1)

# Execute query operations
query_operations()
