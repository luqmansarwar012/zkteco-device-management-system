# Required Imports
from pyairtable import Table
from zk import ZK, const

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

# Adding User Test
checkin_conn = checkin_instance.connect()
checkout_conn = checkout_instance.connect()
checkin_conn.set_user(uid=135, name='Test', privilege=const.USER_DEFAULT, password='', group_id='', user_id='135', card=0)
# checkout_conn.set_user(uid=28, name='Luqmann', privilege=const.USER_DEFAULT, password='', group_id='', user_id='24', card=0)
# checkin_conn.set_user(uid=28, name='Luqman', privilege=const.USER_ADMIN, password='', group_id='', user_id='24', card=0)

# Delete User Test
# checkin_conn.delete_user(user_id=135)
# checkout_conn.delete_user(user_id=24)

# Fingers set
# checkin_users = checkin_conn.get_users()
# checkout_users = checkout_conn.get_users()
# for a in checkout_users:
#     print(a)
# my_user = None
# for user in checkin_users:
#     if user.uid == 28:
#         my_user = user
#         print(f"User match found: {user}")
# checkout_conn.set_user(uid=my_user.uid, name=my_user.name, privilege=my_user.privilege, password=my_user.password, group_id=my_user.group_id, user_id=my_user.user_id, card=my_user.card)
# checkout_users = checkout_conn.get_users()
#
# # Setting fingers
# fingers = checkin_conn.get_templates()
# finger_store = []
# for finger in fingers:
#     if finger.uid == my_user.uid:
#         finger_store.append(finger)
# checkout_conn.save_user_template(my_user, [finger_store[0],finger_store[1]])
# print(finger_store)
# for finger in fingers:
#     print(finger)

# DB TEST
# db_data = table.all()
# db_users = [user['fields'] for user in db_data]
# for user in db_users:
#     print(user)

# get fingers
# checkout_fingers = checkout_conn.get_templates()
# for finger in checkout_fingers:
#     print(finger)

att = checkin_conn.get_attendance()
for at in att:
    print(at)