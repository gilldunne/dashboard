import sys
from pymongo import MongoClient
from datetime import timedelta, datetime

# remove this
client = MongoClient()
db = client.TestEasyJLV

# Establishes a connection to the build job collection in the TestEasyJLV DB
def get_buildjob_db_conn():
    collection = db.buildjob
    return collection

# Loop through each build job on a server and get the last date it was built
def get_end_dates():
    list_of_computer_names = get_computer_names()
    list_of_build_jobs = get_build_jobs()
    collection = get_buildjob_db_conn()
    end_dates_per_server = []
    i = 0
    for computer_name in list_of_computer_names:
        list_of_dates = []
        for job in list_of_build_jobs[i]:
            query = {"computerName": str(computer_name)}
            query.update({"name": str(job)})
            result = collection.find(query, {"endDate": 1}).sort("endDate", -1).limit(1)
            list_of_dates.append(result[0]["endDate"])
        i += 1
        end_dates_per_server.append(list_of_dates)
    return end_dates_per_server

# Checks the date against todays date to see if server is active / inactive
def prepare_graph_data():
    list_of_teams = get_list_teams()
    end_dates_per_server = get_end_dates()
    data = []

    last_seven_days = datetime.today() - timedelta(days=7)
    i = 0
    for team_name in list_of_teams:
        list_data = []
        graph_data = []
        for date_of_build_job in end_dates_per_server[i]:
            if date_of_build_job >= last_seven_days:
                list_data.append(True)
            else:
                list_data.append(False)
        i += 1
        graph_data.append(team_name)
        graph_data.append(list_data)
        data.append(graph_data)
    return data

# Name of the Servers - Domain Names
def get_computer_names():
    collection = get_buildjob_db_conn()
    list_of_computer_names = collection.distinct("computerName")
    return list_of_computer_names


def get_list_teams():
    collection = get_buildjob_db_conn()
    list_of_team_names = collection.distinct("teamName")
    return list_of_team_names


def get_build_job_per_team():
    collection = get_buildjob_db_conn()
    list_of_teams = get_list_teams()
    team_list = []
    for team in list_of_teams:
        buildjob_list = []
        query = collection.find({"teamName": str(team)}).distinct("name")
        x = len(query)
        buildjob_list.append(team)
        # buildjob_list.append(query)
        buildjob_list.append(x)
        team_list.append(buildjob_list)
    return team_list

# Loop through the computer names and get each build job name
def get_build_jobs():
    list_of_computer_names = get_computer_names()
    collection = get_buildjob_db_conn()
    answer = []
    for computer_name in list_of_computer_names:
        result = collection.find({"computerName": str(computer_name)}).distinct("name")
        list_of_build_jobs = []
        for job in result:
            list_of_build_jobs.append(str(job))
        answer.append(list_of_build_jobs)
    return answer

# Get the user and the servers they are connected to
def get_user_data(list_of_computer_names):
    collection = get_buildjob_db_conn()
    user_list = []
    for computer_name in list_of_computer_names:
        query = collection.find({"computerName": str(computer_name)}).distinct("userName")
        user_list.append(computer_name)
        user_list.append(query)
    return user_list

# gets all the users - Not needed perhaps??
def get_users():
    list_of_computer_names = get_computer_names()
    users = get_user_data(list_of_computer_names)
    return users


