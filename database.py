import pyodbc
import os
import datetime
from dotenv import load_dotenv

load_dotenv()


def get_db_connection():
    """Establish a connection to SQL Server using Windows Authentication."""
    server = os.getenv("DB_SERVER")
    database = os.getenv("DB_DATABASE")

    # Windows Authentication uses Trusted_Connection=yes instead of UID/PWD
    conn_str = f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;"

    try:
        conn = pyodbc.connect(conn_str)
        return conn
    except pyodbc.Error as e:
        print(f"Database Connection Error: {e}")
        return None


def fetch_tomorrow_appointments():
    """Get patients with appointments scheduled for tomorrow."""
    conn = get_db_connection()
    if not conn:
        return []

    tomorrow = datetime.date.today() + datetime.timedelta(days=1)

    try:
        cursor = conn.cursor()

        # IMPORTANT: Change 'patients' and the column names below to match your actual SQL Server tables!
        query = """
            SELECT patient_id, full_name, phone_number, next_appointment_date
            FROM patients
            WHERE CAST(next_appointment_date AS DATE) = ?
        """
        cursor.execute(query, tomorrow)

        # Format results as a list of dictionaries
        patients = []
        for row in cursor.fetchall():
            patients.append(
                {
                    "id": row.patient_id,
                    "name": row.full_name,
                    "phone": format_phone(row.phone_number),
                    "date": str(row.next_appointment_date),
                }
            )
        return patients
    finally:
        conn.close()


def fetch_target_audience(segment="All"):
    """Fetch patients based on a marketing segment."""
    conn = get_db_connection()
    if not conn:
        return []

    try:
        cursor = conn.cursor()

        # Fetch patients who have a Zalo User ID (followers)
        query = """
            SELECT full_name, zalo_user_id 
            FROM patients 
            WHERE zalo_user_id IS NOT NULL 
        """

        # Example of filtering by a segment (Adjust 'last_visit_date' to match your database)
        if segment == "Recent Visitors (Last 30 Days)":
            query += " AND last_visit_date >= DATEADD(day, -30, GETDATE())"

        cursor.execute(query)

        patients = []
        for row in cursor.fetchall():
            patients.append({"name": row.full_name, "zalo_id": row.zalo_user_id})
        return patients
    finally:
        conn.close()


def format_phone(phone_str):
    """Format local phone (09...) to Zalo standard (849...)."""
    if not phone_str:
        return ""
    clean = "".join(filter(str.isdigit, str(phone_str)))
    if clean.startswith("0"):
        clean = "84" + clean[1:]
    return clean
