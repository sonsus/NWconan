#python_daemon
#conan.py
import subprocess as sb
import json as j
import http.client
import datetime as dt
from os.path import isfile
from time import sleep, time


'''
whoJson==
    {
        "data":
        "users":
    }

topJson== 
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
    who_parse("whoout")
    return None


def mergeJson(topJson, whoJson): #both param are string
    #mergeJson initialized
    mergeJson="mergeJson.json"
    if not isfile(mergeJson):
        init = open(mergeJson, "w")
        init.close()
        mData=[]
    else:
        with open(mergeJson) as mj: 
            mData=j.load(mj)

    #open topJson and whoJson 
    tj, wj= open(topJson), open(whoJson) 
    tData, wData= j.load(tj), j.load(wj) 

    #1st: remove sysuser from topJson loaded
    for i,obj in enumerate(tData["data"]):
        if obj["user"] not in wData["users"]:
            del tData["data"][i]
    #2nd: append idle whoJson users
    for i,user in enumerate(wData["users"]):
        if user not in tData["users"]:
            tData["users"].append(user)
            tData["data"].append(wData["data"][i])
    wj.close()
    tj.close()

    #3rd: merge it to mergeJson
    tj_w, mj_w = open(topJson,"w"), open(mergeJson,"w") 
    mData.append(tData) 
    del mData[-1]["users"] #now mData==[{"tstmp":tstmp, "data":[obj,obj,...]}] 
    j.dump(tData, tj_w, indent=4)
    j.dump(mData, mj_w, indent=4)
    tj_w.close()
    mj_w.close()


def checkHeavyUser(mergeJson): #Json==filename(str)==mergeJson.json
    #to the top three heavy users, send msg
    with open(mergeJson) as mj:
        mData=j.load(mj)       
        for i in range(3):
            rank=i
            user=mData[-1]["data"][i]["user"]
            cpu =mData[-1]["data"][i]["cpu"] + "%"
            proc=mData[-1]["data"][i]["proc"]
            if not isfile("msg.txt"): 
                with open(msg.txt, "w") as msg:
                    msg.write("To %s (rank=%s): your process %s using %s of the cpu resource \n"%(user,rank,proc,cpu)) 
            sb.run("cat msg.txt | write %s"%user, shell =True) 


def sendJson(Json): # send Json file to http server
    port=8000
    conn=http.client.HTTPConnection("localhost/data:{port}".format(port))
    conn.request("POST", "localhost/data:{port}".format(port), str(j.load(Json)))
    response = conn.getresponse()

    request_res=response.read()
    print(request_res)
    conn.close()

    return None 



def examineSys():
    topJson, whoJson, mergeJson = "topJson.json", "whoJson.json", "mergeJson.json"
    invokeWho()
    invokeTop()
    mergeJson(topJson,whoJson)
    checkHeavyUser(mergeJson)




if __name__=="__main__":
    sb.run("rm mergeJson.json",shell=True)
    start=time()
    while 1: 
        print("Conan.py: Im here for inspect your resource usage")
        examineSys()
        time_elapsed=time()-start
        if time_elapsed%86400==0:
            print("running for %s day(s)"%(time_elapsed/86400))            
            sendJson(mergeJson)
        sleep(500)
