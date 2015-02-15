import json

from bson.json_util import dumps
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Create your views here.
from dashboardIBM import db_wrapper


@api_view(['GET', ])
def get_active_inactive_build_jobs(request):
    """
    <!--  HTML goes here -->
    """
    data = db_wrapper.get_active_inactive_build_jobs()

    return Response(json.loads(dumps(data)))


@api_view(['GET', ])
def get_all_buildjob(request):
    data = db_wrapper.get_all_buildjob()
    return Response(json.loads(dumps(data)))


@api_view(['GET', ])
def get_users(request):
    data = db_wrapper.get_users()
    return Response(json.loads(dumps(data)))