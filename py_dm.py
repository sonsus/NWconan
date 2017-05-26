#python_daemon
#conan.py
import subprocess as sb
import json as j

#def parseJson(rawout):
#    j.dump
#    return Json

def parse_attribute(target, user, cpu, pname, tstmp): #each dtypes are str
	lines_list=target.splitlines()
	

def invokeTop():
    def top_parse(target):
		lines_list=target.splitlines()#list of lines w/o trailing \n	
		dump_list=[]
		with open(topJson.json, "w") as tj:
			for i in range(8,len(lines_list)):                 
				split=lines[i].split()
				obj={}
				obj["user"]=split[1]			#user=col 1
				obj["cpu"]=split[8]				#cpu =col 8
				obj["process_name"]=split[11]	#pname=col 11
				obj["timestamp"]=split[10]		#tstmp=col 10
				dump_list.append(obj)
			tj.dump(dump_list)
		return None

    topout=sb.check_output("top -o %CPU -n 1 -b > topout", shell=True)
    top_parse(topout)
    return None

def invokeWho():
    whoout=sb.check_output("who")
    whoJson=parseJson(whoout)
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

