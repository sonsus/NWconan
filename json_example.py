'''
data.json

[{"title": "foo", "imageData": "xyz123"},
{"title": "bar", "imageData": "abc123"},
{"title": "baz", "imageData": "def456"}]

'''

#removing 'imagedata' in json


import json
with open('data.json') as json_data:
    data = json.load(json_data)
    for element in data: 
        del element['imageData'] 
    print(data)


with open("data.json") as json_data:
    data = json .load(json_data)
    del data[0]
    print(data)