#python_daemon
#conan.py
import subprocess as sb
import shutil as sh
import json as j
import simpleHTTPServer as http
import time

'''
whoJson, topJson== {"data":[obj, obj, obj, obj,...], "users":[user1,user2,user3,...not duplicatively]}
mergeJson== {"data":[obj, obj, obj, obj,...]}
'''

#leaves topJson.json file, return None
def invokeTop():
    def top_parse(target):
		lines_list=target.splitlines()#list of lines w/o trailing \n	
		dump_list=[]

        users_list=[]
		with open("topJson.json", "w") as tj:
			for i in range(8,len(lines_list)):                 
				split=lines[i].split()
				obj={}
				obj["user"]=split[1]			#user=col 1
                users_list.append(obj["user"])
				obj["cpu"]=split[8]				#cpu =col 8
				obj["process_name"]=split[11]	#pname=col 11
#				obj["timestamp"]=split[10]		#tstmp=col 10
				dump_list.append(obj)
			users_list=list(set(users_list))
            wrap_dict={"data":dump_list, "users":users_list}
            tj.dump(wrap_dict)

		return None

    topout=sb.check_output("top -o %CPU -n 1 -b > topout", shell=True)
    top_parse(topout)
    return None

#leaves whoJson.json file, wuser return None
def invokeWho():
    def who_parse(target):
        lines_list=target.splitlines()
        dump_list= []
        users_list= []
        with open("whoJson.json", "w") as wj:
            for line in lines_list:
                obj={}
                obj["user"]=line.split()[0]
                users_list.append(obj["user"])
                obj["cpu"]=None            # defaults to None
                obj["process_name"]=None   
                obj["timestamp"]=None
                dump_list.append(obj)
            users_list=list(set(users_list))
            wrap_dict={"data":dump_list}
            j.dump(wrap_dict,wj)
        return None      

    whoout=sb.check_output("who")
    whoJson=who_parse(whoout)
    return None

def mergeJson(whoJson, topJson): #both param are string
    #top/whoJson.json --> conserved
    mergeJson="mergeJson.json"
    sh.copyfile(topJson,mergeJson)
    with open(whoJson), open(mergeJson) as wj, mj:
        wData, mData=j.load(wj), j.load(mj),
        #remove sysuser
        for i,user in enumerate(mData["users"]):
            if user not in wData["users"]:
                del mData["users"][i]
                del mData["data"][i]
        #append idle whoJson users
        for i,user in enumerate(wData["users"]):
            if user not in mData["users"]:
                mData["users"].append(user)
                mData["data"].append(wData["data"][i])
        del mData["users"] #removing users attribute in mergeJson.json
        # mergeJson--> {"data":[obj, obj, obj, obj,...]}

def checkHeavyUser(Json): #Json==filename(str)==mergeJson.json
	'''
	need to calc sumup %cpu over cumulate json


	'''
	with open(Json) as file:
		Data=j.load(file)
		sum_up={}
		for username in Data["users"]:
			tot_
			sum_up[username]=


	return None 
def sendJson(Json) # send Json file to http server
	#send cumulated Json
	return None 


def saveJson()
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
    while 1:
        time.sleep(300)
        examineSys()