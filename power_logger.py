import requests
import time
import json
import psycopg2
import datetime
import secrets

# Set the variables from secrets.py
host = secrets.host
database = secrets.database
user = secrets.user
password = secrets.password
url = secrets.url


def log_to_database(data):
    time_now = datetime.datetime.now()
    formatted_time = time_now.strftime("%Y-%m-%d %H:%M:%S.%f")
    # print("Incoming data", data)
    # Connect to the database
    try:
        # Connect to the database
        conn = psycopg2.connect(
            host=host,
            database=database,
            user=user,
            password=password
        )

        # Create a cursor object
        cur = conn.cursor()

        # Insert data into the "log" table
        wifi_strength = data["wifi_strength"]
        total_power_import_kwh = float(data["total_power_import_kwh"])
        active_power_w = float(data["active_power_w"])
        active_power_l1_w = float(data["active_power_l1_w"])
        active_power_l2_w = float(data["active_power_l2_w"])
        active_power_l3_w = float(data["active_power_l3_w"])
        active_current_a = float(data["active_current_a"])
        active_current_l1_a = float(data["active_current_l1_a"])
        active_current_l2_a = float(data["active_current_l2_a"])
        active_current_l3_a = float(data["active_current_l3_a"])
        active_voltage_l1_v = float(data["active_voltage_l1_v"])
        active_voltage_l2_v = float(data["active_voltage_l2_v"])
        active_voltage_l3_v = float(data["active_voltage_l3_v"])

        sql = ("INSERT INTO log ( time, wifi_strength, total_power_import_kwh, active_power_w, active_power_l1_w, \
               active_power_l2_w, active_power_l3_w, active_current_a, active_current_l1_a, active_current_l2_a, \
               active_current_l3_a, active_voltage_l1_v, active_voltage_l2_v, active_voltage_l3_v) \
               VALUES (%s, %s, %s, %s,  %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
        values = (formatted_time, wifi_strength, total_power_import_kwh, active_power_w, active_power_l1_w,
                  active_power_l2_w, active_power_l3_w, active_current_a, active_current_l1_a,
                  active_current_l2_a, active_current_l3_a, active_voltage_l1_v, active_voltage_l2_v,
                  active_voltage_l3_v)
        cur.execute(sql, values)
        # print("SQL and values:", sql, values)
        # Commit the changes
        conn.commit()

        print(f"Power: {int(active_power_w)} W")

    except psycopg2.Error as e:
        print("Error:", e)

    finally:
        # Close the cursor and connection
        cur.close()
        conn.close()


while True:
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        log_to_database(data)
    else:
        print("Error:", response.status_code)

    time.sleep(1)  # Wait for 1 seconds before the next request
