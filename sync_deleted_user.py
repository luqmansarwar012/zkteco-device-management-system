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


def sync_deleted_user():
    try:
        print("Delete script running...")
        # connect to devices
        checkout_conn = checkout_instance.connect()
        checkin_conn = checkin_instance.connect()

        # Getting Database users
        db_data = table.all()
        db_users = [user['fields'] for user in db_data]
        # Getting users from checkout device
        checkout_device_users = checkout_conn.get_users()
        # Getting users from checkin device
        checkin_device_users = checkin_conn.get_users()

        # Getting user from Airtable with deleted status to deleted from devices
        for user in db_users:
            if user['sync_status'] == 'deleted':
                checkin_conn.delete_user(user_id=user['user_id'])
                checkout_conn.delete_user(user_id=user['user_id'])

            # For checking which user is present in Airtable but deleted from devices
            else:
                # Checking for checkout device
                checkout_user_exists = False
                for checkout_user in checkout_device_users:
                    if checkout_user.name == user['name']:
                        checkout_user_exists = True
                if not checkout_user_exists:
                    record_id = None
                    for db_user in db_data:
                        if db_user['fields']['name'] == user['name']:
                            record_id = db_user['id']
                    table.update(record_id, {'sync_status': 'deleted'})

                # Checking for checkin device
                checkin_user_exists = False
                for checkin_user in checkin_device_users:
                    if checkin_user.name == user['name']:
                        checkin_user_exists = True
                if not checkin_user_exists:
                    record_id = None
                    for db_user in db_data:
                        if db_user['fields']['name'] == user['name']:
                            record_id = db_user['id']
                    table.update(record_id, {'sync_status': 'deleted'})

    except Exception as e:
        print("Process terminate : {}".format(e))
    finally:
        if checkout_conn:
            checkout_conn.disconnect()
        if checkin_conn:
            checkin_conn.disconnect()
        sync_deleted_user()

sync_deleted_user()