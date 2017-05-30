import json as j
w,t=open("whoJson.json"),open("topJson.json")
print(j.load(t))
print(j.load(w))