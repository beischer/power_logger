import requests
import time
import json
import psycopg2
import datetime

# Replace with your database credentials
host = "localhost"
database = "house_power"
user = "postgres"
password = "Magnus71"

url = "http://192.168.1.215/api/v1/data"


def log_to_database(data):
    time_now = datetime.datetime.now()
    formatted_time = time_now.strftime("%Y-%m-%d %H:%M:%S.%f")
    print("Incoming data", data)
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
        total_power_import_kwh = data["total_power_import_kwh"]
        active_power_w = data["active_power_w"]
        active_power_l1_w = data["active_power_l1_w"]
        active_power_l2_w = data["active_power_l2_w"]
        active_power_l3_w = data["active_power_l3_w"]
        active_current_a = data["active_current_a"]
        active_current_l1_a = data["active_current_l1_a"]
        active_current_l2_a = data["active_current_l2_a"]
        active_current_l3_a = data["active_current_l3_a"]

        sql = ("INSERT INTO log ( time, wifi_strength, total_power_import_kwh, active_power_w, active_power_l1_w, \
               active_power_l2_w, active_power_l3_w, active_current_a, active_current_l1_a, active_current_l2_a, \
               active_current_l3_a) VALUES (%s, %s, %s, %s,  %s, %s, %s, %s, %s, %s, %s)")
        values = (formatted_time, wifi_strength, total_power_import_kwh, active_power_w, active_power_l1_w,
                  active_power_l2_w, active_power_l3_w, active_current_a, active_current_l1_a,
                  active_current_l1_a, active_current_l1_a)
        cur.execute(sql, values)
        # print("SQL and values:", sql, values)
        # Commit the changes
        conn.commit()

        print("Data inserted successfully!")

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

    time.sleep(1)  # Wait for 5 seconds before the next request


#  'wifi_strength': 64, 'total_power_import_kwh': 37835.001,
#  'active_power_w': 4491.0, 'active_power_l1_w': 903.0, 'active_power_l2_w': 1281.0, 'active_power_l3_w': 2306.0,
#  'active_voltage_l1_v': 236.1, 'active_voltage_l2_v': 238.0, 'active_voltage_l3_v': 236.1,
#  'active_current_a': 20.3, 'active_current_l1_a': 4.5, 'active_current_l2_a': 5.9, 'active_current_l3_a': 9.9,

