#python_daemon
#conan.py
import subprocess as sb
import shutil as sh
import json as j
import http
import datetime as dt
from os.path import isfile
from time import sleep



'''
whoJson, topJson== 
    {
        "tstmp: string or None, 
        "data":[obj, obj, obj, obj,...], 
        "users":[user1,user2,user3,...not duplicatively]
    }
mergeJson== 
    [
        {
            "tstmp": tstmp,
            "data":[obj, obj, obj, obj,...]
        },
        {
            "tstmp": tstmp,
            "data":[obj, obj, obj, obj,...]
        },
        {
            "tstmp": tstmp,
            "data":[obj, obj, obj, obj,...]
        },
    ]

'''

#leaves topJson.json file, return None
def invokeTop():
    def top_parse(file, tstmp):
        lines_list=open(file).read().splitlines()#list of lines w/o trailing \n    
        dump_list=[]
        users_list=[]
        with open("topJson.json", "w") as tj:
            for i in range(8,len(lines_list)):                 
                split=lines_list[i].split()
                obj={}
                obj["user"]=split[1]            #user=col 1
                users_list.append(obj["user"])
                obj["cpu"]=split[8]                #cpu =col 8
                obj["process_name"]=split[11]    #pname=col 11
                dump_list.append(obj)
            users_list=list(set(users_list))
            wrap_dict={"tstmp":tstmp, "data":dump_list, "users":users_list}
            j.dump(wrap_dict,tj,indent =4)
        return None

    sb.run("top -o %CPU -n 1 -b>topout", shell=True)
    tstmp=str(dt.datetime.now()).split(".")[0] # yr-mon-dat hr:min:sec
    top_parse("topout",tstmp)
    return None

#leaves whoJson.json file, wuser return None
def invokeWho():
    def who_parse(file):
        lines_list=open(file).read().splitlines()
        dump_list= []
        users_list= []
        with open("whoJson.json", "w") as wj:
            for line in lines_list:
                obj={}
                obj["user"]=line.split()[0]
                users_list.append(obj["user"])
                obj["cpu"]=None            #defaults to None
                obj["process_name"]=None   
                dump_list.append(obj)
            users_list=list(set(users_list))
            wrap_dict={"data":dump_list, "users":users_list}
            j.dump(wrap_dict,wj,indent=4)
        return None      

    sb.run("who > whoout", shell=True)
    whoJson=who_parse("whoout")
    return None

def mergeJson(whoJson, topJson): #both param are string
    #mergeJson initialized
    mergeJson="mergeJson.json"
    if not isfile(mergeJson):
        init=open(merJson, "w")
        j.dump([], init, indent=4)
        init.close()
    #1st: remove sysusers in topJson
    with open(whoJson), open(topJson), open(mergeJson) as wj, tj, mj:
        wData, tData, mData=j.load(wj), j.load(tj), j.load(mj)
        #remove sysuser from topJson loaded
        for i,user in enumerate(mData["users"]):
            if user not in wData["users"]:
                del tData["users"][i]
                del tData["data"][i]
        #append idle whoJson users
        for i,user in enumerate(wData["users"]):
            if user not in tData["users"]:
                tData["users"].append(user)
                tData["data"].append(wData["data"][i])
        j.dump(tData, tj, indent=4)
    #2nd: append it to mergeJson
        del tData["users"] #now tData=={"tstmp":tstmp, "data":[obj,obj,...]} 
        mData.append(tData)
        j.dump(mData,mj,indent=4)

#def checkHeavyUser(Json): #Json==filename(str)==mergeJson.json
    '''
    need to calc sumup %cpu over cumulate json


    '''
#    with open(Json) as file:
#        Data=j.load(file)
#        sum_up={}
#        for username in Data["users"]:
##            tot_
#            sum_up[username]=


    return None 
def sendJson(Json): # send Json file to http server
    #send cumulated Json
    return None 


def saveJson():
    return None 
'''
oneshot-->cumulate
[
    {timestamp, oneshot_list},
    {timestamp, oneshot_list},
    {timestamp, oneshot_list},
]
'''

def examineSys():
    invokeWho()
    invokeTop()
    mergeJson("whoJson.json","topJson.json")



if __name__=="__main__":
    invokeTop()
    invokeWho()