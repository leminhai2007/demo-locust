from locust_plugins.csvreader import CSVDictReader
from os import path, getcwd

users_datasheet = CSVDictReader(path.join(getcwd(), "data", "user.csv"))

def get_user_data():
    user_data = next(users_datasheet)
    return (user_data['username'], user_data['password'])