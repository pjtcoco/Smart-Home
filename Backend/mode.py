# model.py

from firebase_admin import firestore


class Department:
    def __init__(self, id, name):
        self.id = id
        self.name = name
        

    @classmethod
    def get_all(cls):
        departments = []
        # Retrieve department data from Firestore
        # Create Department instances and append to the 'departments' list
        return departments

class Device:
    def __init__(self, id, name, department_id):
        self.id = id
        self.name = name
        self.department_id = department_id

    @classmethod
    def get_by_department(cls, department_id):
        devices = []
        # Retrieve device data from Firestore based on the department_id
        # Create Device instances and append to the 'devices' list
        return devices


