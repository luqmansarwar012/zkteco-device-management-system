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


# Updating devices from database
def db_to_devices():
    try:
        print("Update - Database to devices, script running...")
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

        # Checking for every db user in both devices if changes found update it
        # Outer loop for db user
        for db_user in db_users:
            # Updating in checkout device
            for checkout_user in checkout_device_users:
                if int(checkout_user.user_id) == db_user['user_id']:
                    if checkout_user.name != db_user['name'] or checkout_user.card != db_user['card'] or checkout_user.privilege != int(db_user['privilege']):
                        # Updating user in checkout device
                        checkout_conn.set_user(uid=db_user['uid'], name=db_user['name'], privilege=int(db_user['privilege']), user_id=str(db_user['user_id']), card=db_user['card'])

            #Updating in checkin device
            for checkin_user in checkin_device_users:
                if int(checkin_user.user_id) == db_user['user_id']:
                    if checkin_user.name != db_user['name'] or checkin_user.card != db_user['card'] or checkin_user.privilege != int(db_user['privilege']):
                        # Updating user in checkin device
                        checkin_conn.set_user(uid=db_user['uid'], name=db_user['name'], privilege=int(db_user['privilege']), user_id=str(db_user['user_id']), card=db_user['card'])

    except Exception as e:
        print("Process terminate : {}".format(e))
    finally:
        if checkout_conn:
            checkout_conn.disconnect()
        if checkin_conn:
            checkin_conn.disconnect()
        # db_to_devices()


# Updating Database from Devices
def checkout_to_others():
    try:
        print("Update - Devices to datbase , script running...")
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

        # Checking If Checkout users are different
        for checkout_user in checkout_device_users:
            # Updating db
            for db_user in db_users:
                if checkout_user.uid == db_user['uid']:
                    if checkout_user.name != db_user['name'] or checkout_user.card != db_user[
                        'card'] or checkout_user.privilege != int(db_user['privilege']) or checkout_user.user_id != str(
                        db_user['user_id']):
                        record_id = None
                        for user in db_data:
                            print(user['id'])
                            if user['fields']['name'] == db_user['name']:
                                record_id = user['id']
                        table.update(record_id, {'user_id':int(checkout_user.user_id),"name":checkout_user.name,"card":checkout_user.card,"privilege":str(checkout_user.privilege)})

            # Updating checkin device
            for checkin_user in checkin_device_users:
                if checkin_user.user_id == checkout_user.user_id:
                    if checkin_user.name != checkout_user.name or checkin_user.card != checkout_user.card or checkin_user.privilege != checkout_user.privilege or checkin_user.user_id != checkout_user.user_id:
                        checkin_conn.set_user(uid=checkout_user.uid, name=checkout_user.name, privilege=checkout_user.privilege, password='',
                                              group_id='', user_id=checkout_user.user_id, card=checkout_user.card)

    except Exception as e:
        print("Process terminate : {}".format(e))
    finally:
        if checkout_conn:
            checkout_conn.disconnect()
        if checkin_conn:
            checkin_conn.disconnect()
        checkout_to_others()


# Updating Database from Devices
def checkin_to_others():
    try:
        print("Update - Devices to datbase , script running...")
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


        # Checking if checkin users are different
        for checkin_user in checkin_device_users:
            # for updating db
            for db_user in db_users:
                if checkin_user.uid == db_user['uid']:
                    if checkin_user.name != db_user['name'] or checkin_user.card != db_user[
                        'card'] or checkin_user.privilege != int(
                        db_user['privilege']) or checkin_user.user_id != str(
                        db_user['user_id']):
                        record_id = None
                        for user in db_data:
                            if user['fields']['name'] == db_user['name']:
                                record_id = user['id']
                        table.update(record_id, {'user_id': int(checkin_user.user_id), "name": checkin_user.name,
                                                 "card": checkin_user.card,
                                                 "privilege": str(checkin_user.privilege)})

            # Updating in checkout
            for checkout_user in checkout_device_users:
                if checkout_user.user_id == checkin_user.user_id:
                    if checkin_user.name != checkout_user.name or checkin_user.card != checkout_user.card or checkin_user.privilege != checkout_user.privilege or checkin_user.user_id != checkout_user.user_id:
                        checkout_conn.set_user(uid=checkin_user.uid, name=checkin_user.name,
                                              privilege=checkin_user.privilege, password='',
                                              group_id='', user_id=checkin_user.user_id,
                                              card=checkin_user.card)

    except Exception as e:
        print("Process terminate : {}".format(e))
    finally:
        if checkout_conn:
            checkout_conn.disconnect()
        if checkin_conn:
            checkin_conn.disconnect()
        checkin_to_others()


db_to_devices()
# checkout_to_others()
# checkin_to_others()