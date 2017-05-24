#python_daemon
#conan.py
import subprocess as sb
import json as j

def invokeTop():
    topout=sb.check_output("top").decode("utf-8")
    return topJson

def invokeWho():
    sb.run("who")
    #parse into json
    return whoJson

def mergeJson(whoJson, topJson):
    for user in topJson.users:
        if user not in whoJson.users: 
            #remove the entry for the sysuser
    mergedJson=topJson

    for user in whoJson.users:
        if user not in mergedJson.users:
            #add user merged.users
            #with default field
    return mergedJson

