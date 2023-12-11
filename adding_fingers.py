# Required Imports
import codecs

from zk import ZK, const
from pyairtable import Table
from zk.finger import Finger

# Device Connection Variables
checkout_conn = None
checkin_conn = None

# Instances For Devices:
checkout_instance = ZK('192.168.0.4', port=4370, timeout=5, password=0, force_udp=False, ommit_ping=False)
checkin_instance = ZK('192.168.0.8', port=4370, timeout=5, password=0, force_udp=False, ommit_ping=False)

# Setting up connection to Air Table
# BASE_ID = "appPgvuZjUx3Cp5wZ"
# API_KEY = "keyLlwpXsUSV6wkCU"
# TABLE_NAME = "fingers"
# TABLE_ID = "tbl1jwISQiRwkqGjB"
# table = Table(API_KEY, BASE_ID, TABLE_NAME)

# def fingers_to_database():
#     try:
#         print("Fingers to database script running...")
#         # connect to devices
#         checkout_conn = checkout_instance.connect()
#         checkin_conn = checkin_instance.connect()

#         checkout_fingers = checkout_conn.get_templates()
#         checkin_fingers = checkin_conn.get_templates()

#         print("checkout fingers")
#         for finger in checkout_fingers:
#             print(finger)
#         print("checkin fingers")
#         for finger in checkin_fingers:
#             print(finger)

#         db_data = table.all()
#         db_fingers = [finger['fields'] for finger in db_data]
#         if not db_fingers:
#             # Checkout fingers
#             for finger in checkout_fingers:
#                 data_exists = False
#                 for db_finger in db_fingers:
#                     if db_finger['uid'] == finger.uid:
#                         data_exists = True
#                 if not data_exists:
#                     user_to_add = {'uid': finger.uid,
#                                    'fid': finger.fid,
#                                    'valid': finger.valid,
#                                    'size': finger.size,
#                                    'template': str(finger.template),
#                                    'device':'checkout'}
#                     table.create(user_to_add)
#             # Checkin fingers
#             new_db_data = table.all()
#             new_db_fingers = [finger['fields'] for finger in new_db_data]
#             for finger in checkin_fingers:
#                 data_exists = False
#                 for db_finger in new_db_fingers:
#                     if db_finger['uid'] == finger.uid:
#                         data_exists = True
#                 if not data_exists:
#                     user_to_add = {'uid': finger.uid,
#                                    'fid': finger.fid,
#                                    'valid': finger.valid,
#                                    'size': finger.size,
#                                    'template': str(finger.template),
#                                    'device':'checkin'}
#                     table.create(user_to_add)

#         else:
#             #  For checkout fingers
#             for finger in checkout_fingers:
#                 data_exists = False
#                 for db_finger in db_fingers:
#                     if db_finger['uid'] == finger.uid:
#                         data_exists = True
#                 if not data_exists:
#                     user_to_add = {'uid': finger.uid,
#                                    'fid': finger.fid,
#                                    'valid': finger.valid,
#                                    'size': finger.size,
#                                    'template': str(finger.template),
#                                    'device':'checkout'}
#                     table.create(user_to_add)

#             #  For checkin fingers
#             new_db_data = table.all()
#             new_db_fingers = [finger['fields'] for finger in new_db_data]
#             for finger in checkin_fingers:
#                 data_exists = False
#                 for db_finger in new_db_fingers:
#                     if db_finger['uid'] == finger.uid:
#                         data_exists = True
#                 if not data_exists:
#                     user_to_add = {'uid': finger.uid,
#                                    'fid': finger.fid,
#                                    'valid': finger.valid,
#                                    'size': finger.size,
#                                    'template': str(finger.template),
#                                    'device':'checkin'}
#                     table.create(user_to_add)

#     except Exception as e:
#         print("Process terminate : {}".format(e))
#     finally:
#         if checkout_conn:
#             checkout_conn.disconnect()
#         if checkin_conn:
#             checkin_conn.disconnect()
#         # fingers_to_database()

# # fingers_to_database()


# def fingers_device_sync():
#     try:
#         print("Fingers script running...")
#         # connect to devices
#         checkout_conn = checkout_instance.connect()
#         checkin_conn = checkin_instance.connect()

#         # Getting checkout users
#         checkout_users = checkout_conn.get_users()
#         checkin_users = checkin_conn.get_users()

#         # For syncing fingers from checkout device
#         for checkout_user in checkout_users:

#             # getting checkout fingers to store in checkin
#             checkout_fingers = checkout_conn.get_templates()

#             # for storing finger of particular user
#             finger_store = []
#             for finger in checkout_fingers:
#                 if finger.uid == checkout_user.uid:
#                     finger_store.append(finger)

#             # Storing saved finger into corresponding user
#             for checkin_user in checkin_users:
#                 if checkin_user.uid == checkout_user.uid:

#                     # Getting checkin fingers to check if exists already
#                     checkin_fingers = checkin_conn.get_templates()
#                     finger_check = False
#                     for finger in checkin_fingers:
#                         if finger.uid == checkin_user.uid:
#                             finger_check = True

#                     # If fingers not found in checkin device
#                     if not finger_check:
#                         checkin_conn.save_user_template(checkin_user, [finger_store[0], finger_store[1]])

#         # For syncing fingers from checkin device
#         for checkin_user in checkin_users:

#             # getting checkout fingers to store in checkout
#             checkin_fingers = checkin_conn.get_templates()

#             # for storing finger of particular user
#             finger_store = []
#             for finger in checkin_fingers:
#                 if finger.uid == checkin_user.uid:
#                     finger_store.append(finger)

#             # Storing saved finger into corresponding user
#             for checkout_user in checkout_users:
#                 if checkin_user.uid == checkout_user.uid:

#                     # Getting checkout fingers to check if exists already
#                     checkout_fingers = checkout_conn.get_templates()
#                     finger_check = False
#                     for finger in checkout_fingers:
#                         if finger.uid == checkout_user.uid:
#                             finger_check = True

#                     # If fingers not found in checkin device
#                     if not finger_check:
#                         checkout_conn.save_user_template(checkout_user, [finger_store[0], finger_store[1]])
#             print(finger_store)



#     except Exception as e:
#         print("Process terminate : {}".format(e))
#     finally:
#         if checkout_conn:
#             checkout_conn.disconnect()
#         if checkin_conn:
#             checkin_conn.disconnect()
#         # fingers_device_sync()

# # fingers_device_sync()

# def fingers_from_database():
#     try:
#         print("Fingers to database script running...")
#         # connect to devices
#         checkout_conn = checkout_instance.connect()
#         checkin_conn = checkin_instance.connect()

#         # Geting device users
#         checkout_users = checkout_conn.get_users()
#         checkin_users = checkin_conn.get_users()

#         # Getting device fingers
#         checkin_fingers = checkin_conn.get_templates()
#         checkout_fingers = checkout_conn.get_templates()

#         # Getting database fingers
#         db_data = table.all()
#         db_fingers = [finger['fields'] for finger in db_data]

#         # For Checkout device
#         for db_finger in db_fingers:
#             checkout_finger_check = False
#             # To check if fingerprints are present in checkout device already.
#             for checkout_finger in checkout_fingers:
#                 if checkout_finger.uid == db_finger['uid']:
#                     checkout_finger_check = True
#                     print(f"data with {checkout_finger.uid} uid exists already!")

#             # If not present already
#             if not checkout_finger_check:
#                 print(f"code check: {db_finger['uid']}")
#                 finger_store = []
#                 # Getting the user against finger uid to save in device
#                 for checkout_user in checkout_users:
#                     print(f"code check checkout loop: {db_finger['uid']}")
#                     if checkout_user.uid == db_finger['uid']:
#                         print(f"code check checkout loop: {db_finger['uid']}, found user {checkout_user.uid}")
#                         #To get all the fingers for that user
#                         for finger in db_fingers:
#                             if finger['uid'] == checkout_user.uid:
#                                 # Generating finger object using db attributes
#                                 fingerObj = Finger(finger['uid'], finger['fid'], finger['valid'], bytes(finger['template'],encoding="ascii"))
#                                 print(fingerObj)
#                                 finger_store.append(fingerObj)
#                         print(f"finger saved of {checkout_user.uid} name: {checkout_user.name}")
#                         checkout_conn.save_user_template(checkout_user, finger_store)

#     except Exception as e:
#         print("Process terminate : {}".format(e))
#     finally:
#         if checkout_conn:
#             checkout_conn.disconnect()
#         if checkin_conn:
#             checkin_conn.disconnect()
#         # fingers_from_database()

# # fingers_from_database()

checkout_conn = checkout_instance.connect()
fingers = checkout_conn.get_templates()
for finger in fingers:
    print(finger)
