from email.utils import parsedate
import os
import json
from posixpath import split
from time import sleep
import config

key = config.getAPIkey()


def curlAPI(input):
    os.system(input + "> output")

    f = open("output","r+")
    data =json.loads(f.read())
    f.close()
    return data # is a dict

def getVehicleMakes():
    data = curlAPI('curl "https://www.carboninterface.com/api/v1/vehicle_makes" -s -H "Authorization: Bearer '+key+'" -H "Content-Type: application/json" -X GET')
    
    parsed = {}
    ctr=0
    for e in data:
        a = e['data']['attributes']['name']
        b = e['data']['id']
        parsed[ctr]={'name':a,'id':b}
        ctr+=1
    return parsed
    
def getID(parsed, keyword):
    print("What {} is your vehicle?".format(keyword))
    sleep(1)
    for item in parsed:
        print(str(item) + ": " + parsed[item]['name'])

    isInt=False
    while not isInt:
        try:
            index = int(input("\n{} number: ".format(keyword)))
            isInt=True
        except:
            pass
    return parsed[index]['id']

def getVehicleModels(id):
    data = curlAPI('curl "https://www.carboninterface.com/api/v1/vehicle_makes/{}/vehicle_models" -s -H "Authorization: Bearer {}" -H "Content-Type: application/json" -X GET'.format(id,key))

    parsed = {}
    ctr=0
    for e in data:
        a = e['data']['attributes']['vehicle_make']+" "+e['data']['attributes']['name']+" "+str(e['data']['attributes']['year'])
        b = e['data']['id']
        parsed[ctr]={'name':a,'id':b}
        ctr+=1
    return parsed

def getDistAttr(id):
    dist = input("How far will you travel? (mi/km): ")
    user = dist.split(" ")
    give = 'curl "https://www.carboninterface.com/api/v1/estimates" -s -H "Authorization: Bearer '+key+'" -H "Content-Type: application/json" -X POST -d \'{"type": "vehicle", "distance_unit": "'+user[1]+'", "distance_value": '+user[0]+', "vehicle_model_id": "'+str(id)+'"}\''
    data = curlAPI(give)
    return data['data']['attributes']

    
def main():
    parsed = getVehicleMakes()
    id = getID(parsed, "make")
    os.system("clear")
    parsed = getVehicleModels(id)
    id = getID(parsed, "model")
    parsed = getDistAttr(id)
    print("Travelling {} {} in a {} {} {} will release {} pounds of CO2 into the atmosphere.".format(parsed['distance_value'],parsed['distance_unit'],parsed['vehicle_make'],parsed['vehicle_model'],parsed['vehicle_year'],parsed['carbon_lb']))


if __name__ == "__main__":
    main()
