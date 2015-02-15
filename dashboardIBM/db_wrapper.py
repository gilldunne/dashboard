import sys
from pymongo import MongoClient
from datetime import timedelta, datetime

# remove this
client = MongoClient()
db = client.TestEasyJLV

#
# This should only contain read / writes to the DB
# Not currently set that way due to many migration errors
#
# class DBWrapper:
#     client = MongoClient()
#     db = client.TestEasyJLV
#
#     # Open a connection to TestEasyJLV
#     def db_open(self):
#         return self.db
#
#     # Close connection to TestEasyJLV
#     def db_close(self):
#         self.db_close()
#
#     # Use buildjob collection from TestEasyJLV
#     def get_build_job_collection(self):
#         return self.db.buildjob

# Establishes a connection to the build job collection in the TestEasyJLV DB
def get_buildjob_db_conn():
    collection = db.buildjob
    return collection

# Gets the data to display the active and inactive servers and returns it to the view
def get_active_inactive_build_jobs():
    list_of_computer_names = get_computer_names()
    list_of_build_jobs = get_build_jobs(list_of_computer_names)
    end_dates_per_server = get_end_dates(list_of_computer_names, list_of_build_jobs)
    graph_data = prepare_graph_data(list_of_computer_names, end_dates_per_server)
    return graph_data

# Loop through each build job on a server and get the last date it was built
def get_end_dates(list_of_computer_names, list_of_build_jobs):
    collection = get_buildjob_db_conn()
    end_dates_per_server = []
    i = 0
    for computer_name in list_of_computer_names:
        list_of_dates = []
        for job in list_of_build_jobs[i]:
            query = {"computerName": str(computer_name)}
            query.update({"name": str(job)})
            result = collection.find(query, {"endDate": 1}).sort("endDate", -1).limit(1)
            # print >> sys.stderr, "Job: " + str(job)
            # print >> sys.stderr, "End Date: " + str(result[0]["endDate"])
            list_of_dates.append(result[0]["endDate"])
        i += 1
        # print >> sys.stderr, "* * * * * * * * * * * * * * * * * * * * * "
        end_dates_per_server.append(list_of_dates)
    return end_dates_per_server

# Checks the date against todays date to see if server is active / inactive
def prepare_graph_data(list_of_computer_names, end_dates_per_server):
    graph_data = []
    last_seven_days = datetime.today() - timedelta(days=7)
    i = 0
    for computer_name in list_of_computer_names:
        list_data = []
        for date_of_build_job in end_dates_per_server[i]:
            if date_of_build_job >= last_seven_days:
                list_data.append(True)
            else:
                list_data.append(False)
        i += 1
        graph_data.append(computer_name)
        graph_data.append(list_data)
    return graph_data

# Name of the Servers
def get_computer_names():
    collection = get_buildjob_db_conn()
    list_of_computer_names = collection.distinct("computerName")
    return list_of_computer_names

# Gets the number of all the buildjob per team and returns to the view
def get_all_buildjob():
    list_of_computer_names = get_computer_names()
    list_of_build_jobs = get_build_jobs(list_of_computer_names)
    total_number_buildjob = get_total_number_buildjob(list_of_computer_names, list_of_build_jobs)
    return total_number_buildjob

# Loop through the computer names and get each build job name
def get_build_jobs(list_of_computer_names):
    collection = get_buildjob_db_conn()
    answer = []
    for computer_name in list_of_computer_names:
        result = collection.find({"computerName": str(computer_name)}).distinct("name")
        list_of_build_jobs = []
        for job in result:
            list_of_build_jobs.append(str(job))
        answer.append(list_of_build_jobs)
    return answer

# Loop through the computers and get the number of buildjobs in that domain
def get_total_number_buildjob(list_of_computer_names, list_of_build_jobs):
    collection = get_buildjob_db_conn()
    buildjob_list = []
    for computer_name in list_of_computer_names:
        query = collection.find({"computerName": str(computer_name)}).distinct("name")
        x = len(query)
        buildjob_list.append(computer_name)
        buildjob_list.append(query)
        buildjob_list.append(x)
    return buildjob_list

# TODO - Get number active servers for the graph
def get_number_active_servers():

    return None

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


