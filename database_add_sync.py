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


def database_users():
    try:
        print("Database script running...")
        # connect to devices
        checkout_conn = checkout_instance.connect()
        checkin_conn = checkin_instance.connect()

        # Getting users from checkout device
        checkout_device_users = checkout_conn.get_users()
        # Getting users from checkin device
        checkin_device_users = checkin_conn.get_users()

        # Getting Database users
        db_data = table.all()
        db_users = [user['fields'] for user in db_data]

        # External loop for iterating over each db user
        for user in db_users:
            if user['sync_status'] == 'enrolled':
                # Internal loop for adding db user into checkout device
                checkout_user_exists = False
                for checkout_user in checkout_device_users:
                    if user['name'] == checkout_user.name:
                        checkout_user_exists = True
                if not checkout_user_exists:
                    checkout_conn.set_user(uid=user['uid'], name=user['name'], privilege=int(user['privilege']),
                                           password='', user_id=str(user['user_id']))

                # Internal loop for adding db user into checkin device
                checkin_user_exists = False
                for checkin_user in checkin_device_users:
                    if user['name'] == checkin_user.name:
                        checkin_user_exists = True
                if not checkin_user_exists:
                    checkin_conn.set_user(uid=user['uid'], name=user['name'], privilege=int(user['privilege']),
                                           password='', user_id=str(user['user_id']))

    except Exception as e:
        print("Process terminate : {}".format(e))
    finally:
        if checkout_conn:
            checkout_conn.disconnect()
        if checkin_conn:
            checkin_conn.disconnect()
        database_users()


database_users()