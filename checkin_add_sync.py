# Required Imports
from zk import ZK, const
from pyairtable import Table
# import redis

# Redis Connection:
# redis_host = "localhost"
# redis_port = 6379
# r_handler = redis.StrictRedis(host=redis_host,port=redis_port,decode_responses=True)
# lock = r_handler.lock('my_lock')

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


def checkin_device():
    try:
        print(f"Checkin script running...")
        # connect to devices
        checkout_conn = checkout_instance.connect()
        checkin_conn = checkin_instance.connect()

        # Getting users from checkin device to add new users into database and checkout device
        checkin_device_users = checkin_conn.get_users()
        checkout_device_users = checkout_conn.get_users()

        # Getting Database users
        db_data = table.all()
        db_users = [user['fields'] for user in db_data]


        # External loop for checking every device user:
        for checkin_device_user in checkin_device_users:
            checkin_user_exists = False
            # Internal loop for searching device user in database
            for user in db_users:
                if user['uid'] == checkin_device_user.uid:
                    checkin_user_exists = True
                    # If user is found in database but status is deleted
                    if user['sync_status'] == 'deleted':
                        record_id = None
                        for db_user in db_data['records']:
                            if db_user['fields']['name'] == user['name']:
                                record_id = db_user['id']
                        table.update(record_id, {'sync_status': 'enrolled'})

            # If device user is not found in database:
            if not checkin_user_exists:
                if checkin_device_user.privilege == const.USER_ADMIN:
                    privilege = 'Admin'
                user_to_add = {'uid': checkin_device_user.uid,
                               'user_id': int(checkin_device_user.user_id),
                               'name': checkin_device_user.name, 'card': checkin_device_user.card,
                               'privilege': str(checkin_device_user.privilege),
                               'password': checkin_device_user.password,
                               'sync_status':'enrolled'}
                table.create(user_to_add)

            # If device user is found in database
            else:
                print(
                    f"User with user_id: {checkin_device_user.user_id} already exists in checkin device's database!")

            # Internal loop for checking every checkin user in checkout device
            checkout_user_exists = False
            for checkout_device_user in checkout_device_users:
                if checkout_device_user.uid == checkin_device_user.uid:
                    checkout_user_exists = True
            if not checkout_user_exists:
                # Setting User to new device
                checkout_conn.set_user(uid=checkin_device_user.uid, name=checkin_device_user.name,
                                       privilege=const.USER_DEFAULT,
                                       password=checkin_device_user.password,
                                       user_id=checkin_device_user.user_id)
                print("user added")

    except Exception as e:
        print("Process terminate : {}".format(e))
    finally:
        if checkout_conn:
            checkout_conn.disconnect()
        if checkin_conn:
            checkin_conn.disconnect()
        checkin_device()


checkin_device()