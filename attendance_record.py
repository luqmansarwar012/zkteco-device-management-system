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
TABLE_NAME = "attendance"
TABLE_ID = "tblH646KjzCatdyL7"
table = Table(API_KEY, BASE_ID, TABLE_NAME)

def attendance_record():
    try:
        print("Attendance script running...")
        # connect to devices
        checkout_conn = checkout_instance.connect()
        checkin_conn = checkin_instance.connect()

        # Getting users from checkout device
        checkout_device_users = checkout_conn.get_users()
        # Getting users from checkin device
        checkin_device_users = checkin_conn.get_users()

        # Getting Database users
        db_data = table.all()
        db_attendance = [attendance['fields'] for attendance in db_data]

        # Getting Attendance
        checkout_attendance = checkout_conn.get_attendance()
        checkin_attendance = checkin_conn.get_attendance()

        # If there is no attendance record in AirTable
        if not db_attendance:
            for attendance in checkout_attendance:
                my_user = None
                for user in checkout_device_users:
                    if attendance.user_id == user.user_id:
                        my_user = user.name
                dt = attendance.timestamp
                data_to_add = {"uid": attendance.uid, "user_id": int(attendance.user_id),"name":my_user ,"date": dt.strftime("%Y/%m/%d"), "time": dt.strftime("%H:%M:%S"),
                               "status": attendance.status,"device":"checkout"}
                table.create(data_to_add)
            for attendance in checkin_attendance:
                my_user = None
                for user in checkin_device_users:
                    if attendance.user_id == user.user_id:
                        my_user = user.name
                dt = attendance.timestamp
                data_to_add = {"uid": attendance.uid, "user_id": int(attendance.user_id),"name":my_user ,"date": dt.strftime("%Y/%m/%d"), "time": dt.strftime("%H:%M:%S"),
                               "status": attendance.status,"device":"checkin"}
                table.create(data_to_add)
        # If there is attendance record in AirTable
        if db_attendance:
            # Adding checkout new attendance not present already into AirTable
            for attendance in checkout_attendance:
                attendance_exists = False
                for db_att in db_attendance:
                    if db_att['uid'] == attendance.uid:
                        attendance_exists = True
                print(f"Availability: {attendance_exists}")
                if not attendance_exists:
                    my_user = None
                    for user in checkout_device_users:
                        if attendance.user_id == user.user_id:
                            my_user = user.name
                    dt = attendance.timestamp
                    data_to_add = {"uid": attendance.uid, "user_id": int(attendance.user_id), "name": my_user,
                                   "date": dt.strftime("%Y/%m/%d"), "time": dt.strftime("%H:%M:%S"),
                                   "status": attendance.status,"device":"checkout"}
                    table.create(data_to_add)

            # Adding checkout new attendance not present already into AirTable
            for attendance in checkin_attendance:
                attendance_exists = False
                for db_att in db_attendance:
                    if db_att['uid'] == attendance.uid:
                        attendance_exists = True
                print(f"Availability: {attendance_exists}")
                if not attendance_exists:
                    my_user = None
                    for user in checkin_device_users:
                        if attendance.user_id == user.user_id:
                            my_user = user.name
                    dt = attendance.timestamp
                    data_to_add = {"uid": attendance.uid, "user_id": int(attendance.user_id), "name": my_user,
                                   "date": dt.strftime("%Y/%m/%d"), "time": dt.strftime("%H:%M:%S"),
                                   "status": attendance.status,"device":"checkin"}
                    table.create(data_to_add)

    except Exception as e:
        print("Process terminate : {}".format(e))
    finally:
        if checkout_conn:
            checkout_conn.disconnect()
        if checkin_conn:
            checkin_conn.disconnect()
        attendance_record()


attendance_record()