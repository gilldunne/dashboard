import json

from bson.json_util import dumps
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Create your views here.
import sys
from dashboardIBM import db_wrapper

# TODO - Need to get the figures correct here
# Should show the active and inactive numbers
# only shows the active currently
@api_view(['GET', ])
def get_active_inactive_build_jobs(request):
    """
    <!--  HTML goes here -->
    """
    test = []
    act = ""
    data = db_wrapper.prepare_graph_data()
    # print >> sys.stderr, type(data)
    # for i in data:
    #     print >> sys.stderr, i
    #     amt = 0
    #     for j in i:
    #         if(j == True):
    #             amt += 1
    #             act = "active"
    #         elif(j == False):
    #             amt += 1
    #             act = "inactive"
    #     test.append(act)
    #     test.append(amt)
    # json.loads(dumps(data))
    return Response(data)


@api_view(['GET', ])
def get_all_buildjob(request):
    data = db_wrapper.get_build_job_per_team()
    return Response(json.loads(dumps(data)))


@api_view(['GET', ])
def get_users(request):
    data = db_wrapper.get_users()
    return Response(json.loads(dumps(data)))