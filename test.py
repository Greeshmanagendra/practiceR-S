import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from practice import Base, Corporate, Employee, insert_corporate, insert_employee, delete_corporate, delete_employee, update_employee, query_operations

@pytest.fixture(scope='module')
def setup_db():
    # Create an in-memory SQLite database
    engine = create_engine('sqlite:///:memory:', echo=False)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    
    # Yield the session to be used in the test cases
    yield session
    
    # Clean up the database
    session.close()
    Base.metadata.drop_all(engine)

def test_insert_corporate(setup_db):
    session = setup_db
    # Insert corporate data
    insert_corporate('TechCorp', 'New York')
    corporate = session.query(Corporate).filter_by(name='TechCorp').first()
    assert corporate is not None
    assert corporate.name == 'TechCorp'
    assert corporate.location == 'New York'

def test_insert_employee(setup_db):
    session = setup_db
    # Insert corporate and employee data
    insert_corporate('TechCorp', 'New York')
    corporate = session.query(Corporate).filter_by(name='TechCorp').first()
    insert_employee('Alice', 30, corporate.id)
    
    employee = session.query(Employee).filter_by(name='Alice').first()
    assert employee is not None
    assert employee.name == 'Alice'
    assert employee.age == 30
    assert employee.corporate_id == corporate.id

def test_update_employee(setup_db):
    session = setup_db
    # Insert corporate and employee data
    insert_corporate('TechCorp', 'New York')
    corporate = session.query(Corporate).filter_by(name='TechCorp').first()
    insert_employee('Alice', 30, corporate.id)
    
    # Update employee
    employee = session.query(Employee).filter_by(name='Alice').first()
    update_employee(employee.id, name='Alice Updated', age=35, corporate_id=corporate.id)
    
    updated_employee = session.query(Employee).filter_by(id=employee.id).first()
    assert updated_employee.name == 'Alice Updated'
    assert updated_employee.age == 35

def test_delete_employee(setup_db):
    session = setup_db
    # Insert corporate and employee data
    insert_corporate('TechCorp', 'New York')
    corporate = session.query(Corporate).filter_by(name='TechCorp').first()
    insert_employee('Alice', 30, corporate.id)
    
    # Delete employee
    employee = session.query(Employee).filter_by(name='Alice').first()
    delete_employee(employee.id)
    
    deleted_employee = session.query(Employee).filter_by(id=employee.id).first()
    assert deleted_employee is None

def test_delete_corporate(setup_db):
    session = setup_db
    # Insert corporate data
    insert_corporate('TechCorp', 'New York')
    
    # Delete corporate
    corporate = session.query(Corporate).filter_by(name='TechCorp').first()
    delete_corporate(corporate.id)
    
    deleted_corporate = session.query(Corporate).filter_by(id=corporate.id).first()
    assert deleted_corporate is None

def test_query_operations(setup_db):
    session = setup_db
    # Insert corporate and employee data
    insert_corporate('TechCorp', 'New York')
    insert_corporate('HealthInc', 'San Francisco')
    tech_corp = session.query(Corporate).filter_by(name='TechCorp').first()
    health_inc = session.query(Corporate).filter_by(name='HealthInc').first()
    
    insert_employee('Alice', 30, tech_corp.id)
    insert_employee('Bob', 25, health_inc.id)
    insert_employee('Charlie', 30, tech_corp.id)
    
    # Perform query operations
    results = query_operations()
    
    assert len(results) > 0  # Check if results were returned
