from fastapi import FastAPI
from database import get_db_connection

app = FastAPI()


@app.get("/")
def home():

    return {"message": "Employee Management API"}


@app.get("/employees")
def get_employees():

    conn = get_db_connection()

    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM employee")

    employees = cursor.fetchall()

    cursor.close()

    conn.close()

    return employees
