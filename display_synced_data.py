# Required Imports
import requests
from zk import ZK, const
from pyairtable import Table

# Device Connection Variables
checkout_conn = None
checkin_conn = None

# Instances For Devices:
checkout_instance = ZK('192.168.0.4', port=4370, timeout=5, password=0, force_udp=False, ommit_ping=False)
checkin_instance = ZK('192.168.0.8', port=4370, timeout=5, password=0, force_udp=False, ommit_ping=False)

# Setting up connection to Air Table
BASE_ID = "appPgvuZjUx3Cp5wZ"
API_KEY = "keyLlwpXsUSV6wkCU"
TABLE_NAME = "users"
TABLE_ID = "tblpzxpSjU7fxJMi6"
table = Table(API_KEY, BASE_ID, TABLE_NAME)
TABLE_NAME2 = "fingers"
TABLE_ID2 = "tbl1jwISQiRwkqGjB"
fingers_table = Table(API_KEY, BASE_ID, TABLE_NAME2)

def display_synced_data():
    try:
        print("Display script running...")
        # connect to devices
        checkout_conn = checkout_instance.connect()
        checkin_conn = checkin_instance.connect()

        # Getting users from checkout device
        checkout_device_users = checkout_conn.get_users()
        # Getting users from checkin device
        checkin_device_users = checkin_conn.get_users()

        # Getting database users to compare with device users
        # Getting Database users
        db_data = table.all()
        db_users = [user['fields'] for user in db_data]

        # Getting Fingers
        checkout_fingers = checkout_conn.get_templates()
        checkin_fingers = checkin_conn.get_templates()
        db_fingers_data = fingers_table.all()
        db_fingers = [finger['fields'] for finger in db_fingers_data]

        # Display
        print("<----||---->")
        print(f"Checkout users: {len(checkout_device_users)}")
        for user in checkout_device_users:
            print(user)
        print("<----||---->")
        print(f"Checkin users: {len(checkin_device_users)}")
        for user in checkin_device_users:
            print(user)
        print("<----||---->")
        print(f"Database users: {len(db_users)}")
        for user in db_users:
            print(user)
        print("<----||---->")
        # print(f"Database fingers: {len(db_fingers)}")
        # for finger in db_fingers:
        #     print(finger)
        print("<----||---->")
        print("<----||---->")
        print(f"Checkout fingers: {len(checkout_fingers)}")
        for finger in checkout_fingers:
            print(finger)
        print("<----||---->")
        print("<----||---->")
        print(f"Checkin fingers: {len(checkin_fingers)}")
        for finger in checkin_fingers:
            print(finger)
        print("<----||---->")

    except Exception as e:
        print("Process terminate : {}".format(e))
    finally:
        if checkout_conn:
            checkout_conn.disconnect()
        if checkin_conn:
            checkin_conn.disconnect()
        # display_synced_data()


display_synced_data()