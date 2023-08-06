# -*- coding: utf-8 -*-

import os
import sys
import requests
import base64

import shutil
import json
from pathlib import Path
from subprocess import check_output
import platform
import ctypes

from jarvis_sdk import jarvis_config
from jarvis_sdk import jarvis_auth
from jarvis_sdk import jarvis_misc

def display_configuration_deploy_help(jarvis_configuration, firebase_user):

    try:

        # Get UID
        #
        uid = firebase_user["userId"]

        # Get default project
        #
        default_project = (jarvis_config.get_jarvis_configuration_file())["gcp_default_project"]

        url = jarvis_configuration["jarvis_api_endpoint"] + "configuration/help"
        data = {
            "payload": {
                "resource": "help",
                "uid" : uid,
                "gcp_project_id" : default_project
            }
        }
        headers = {
            "Content-type": "application/json",
            "Authorization": "Bearer " + firebase_user["idToken"]
        }

        r = requests.post(url, headers=headers, data=json.dumps(data))

        if r.status_code != 200:
            # print(r.headers)
            print("\nError : %s\n" % str(r.content, "utf-8"))
        else:
            response = r.json()
            print(response["payload"]["help"])

    except Exception as ex:
        print("Error while trying to contact Jarvis API ...")
        print(ex)
        return False

    return True


def process_sql_query(read_configuration, input_conf_file):

    # Get path
    #
    filepath = os.path.dirname(input_conf_file)
    print("File path : {}".format(filepath))

    # Read associated SQL file
    #
    host_system = jarvis_misc.check_platform()

    path_element = None
    if (host_system == "Linux") or (host_system == "Darwin"):
        path_element = "/"
    elif host_system == "Windows":
        path_element = "\\"
    else:
        print("Host OS unknown, cannot process SQL file reading.")
        return None

    sql_full_filename = filepath + path_element + read_configuration["sql_file"]
    print("SQL file path : {}".format(sql_full_filename))

    try:
        with open(sql_full_filename, "r") as f:
            read_sql_file = f.read()
    except Exception as ex:
        print("Error while reading SQL file : " + ex)
        return None

    # Convert SQL query into Base64
    #
    read_sql_file = bytes(read_sql_file, "utf-8")
    return str(base64.b64encode(read_sql_file), "utf-8")

def deploy_configuration(input_conf_file, gcp_project_id, jarvis_configuration, firebase_user):

    # Check if the file exists
    #
    if os.path.isfile(input_conf_file) is False:
        print("File \"%s\" does not exists." % input_conf_file)
        return False

    # Read file and parse it as JSON
    #
    read_configuration = None
    try:
        with open(input_conf_file, "r") as f:
            read_configuration = json.load(f)
    except Exception as ex:
        print("Error while parsing configuration file.")
        return False

    # Special processing for :
    # table-to-storage
    #
    if read_configuration["configuration_type"] == "table-to-storage":
        sql_query = process_sql_query(read_configuration, input_conf_file)
        if sql_query is None:
            return False

        read_configuration["sql"] = sql_query
        del read_configuration["sql_file"]


    # Call API
    #
    try:

        url = jarvis_configuration["jarvis_api_endpoint"] + "configuration"
        data = {
            "payload": {
                "resource": read_configuration,
                "gcp_project_id" : gcp_project_id,
                "uid" : firebase_user["userId"]
            }
        }
        headers = {
            "Content-type": "application/json",
            "Authorization": "Bearer " + firebase_user["idToken"
            ]}

        r = requests.put(url, headers=headers, data=json.dumps(data))

        # if response.status_code != 200 :
        #     print("API returned an error.")
        #     print(response.json())
        #     return False

        if r.status_code != 200:
            # print(r.headers)
            print("\nError : %s\n" % str(r.content, "utf-8"))
            return False
        else:
            response = r.json()
            print(response["payload"]["message"])
            return True

    except Exception as ex:
        print("Error while trying to contact Jarvis API ...")
        print(ex)
        return False


def process_gcp_project_id(gcp_pid, default_pid):
    if gcp_pid is None:
        print("Using default GCP Project ID : %s" % default_pid)
        return default_pid
    else:
        print("Using provided GCP Project ID : %s" % gcp_pid)
        return gcp_pid


def process(args):

    print("Jarvis Configuration Manager.")

    # Get configuration
    #
    jarvis_configuration = jarvis_config.get_jarvis_configuration_file()

    # Get firebase user
    #
    firebase_user = jarvis_auth.get_refreshed_firebase_user(jarvis_configuration)

    # Process GCP project ID
    #
    gcp_project_id = process_gcp_project_id(args.gcp_project_id, jarvis_configuration["gcp_default_project"])

    if args.command == "deploy":
        if len(args.arguments) >= 2:
            if args.arguments[1] is not None:
                if args.arguments[1] == "help":
                    return display_configuration_deploy_help(jarvis_configuration, firebase_user)
                else:
                    return deploy_configuration(args.arguments[1],gcp_project_id, jarvis_configuration, firebase_user)
            else:
                print("Argument unknown." % args.arguments[1])
                return False
        else:
            return display_configuration_deploy_help(jarvis_configuration, firebase_user)

    return True
