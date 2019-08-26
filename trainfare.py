from flask import Flask
from flask import request
from flask import make_response
import json
import requests

#flask set up
app = Flask(__name__)
@app.route('/fare', methods=["GET","POST"])
def fare():
    req = request.get_json(silent=True, force=True)
    intent_name = req["queryResult"]["intent"]["displayName"]
    if intent_name == 'fare':
        return train_fare(req,intent_name)
    elif intent_name == 'location':
        return location(req, intent_name)
    elif intent_name == 'sourcedest':
        return src_dest(req, intent_name)


def train_fare(req, intent_name):
    no = str(req["queryResult"]["parameters"]["number"])
    quota = req["queryResult"]["parameters"]["quota"]
    action = req["queryResult"]["action"]
    if quota == 'AC First Class':
        response = requests.get('http://indianrailapi.com/api/v2/TrainFare/apikey/f0b655638770e7ffc18f1dcef0385648/TrainNumber/12565/From/SEE/To/NDLS/Quota/AC First Class').json()
        f = response["Fares"][0]["Fare"]
    elif quota == 'AC 2-Tier':
        response = requests.get('http://indianrailapi.com/api/v2/TrainFare/apikey/f0b655638770e7ffc18f1dcef0385648/TrainNumber/12565/From/SEE/To/NDLS/Quota/AC 2-Tier').json()
        f = response["Fares"][1]["Fare"]
    elif quota == 'AC 3-Tier':
        response = requests.get('http://indianrailapi.com/api/v2/TrainFare/apikey/f0b655638770e7ffc18f1dcef0385648/TrainNumber/12565/From/SEE/To/NDLS/Quota/AC 3-Tier').json()
        f = response["Fares"][2]["Fare"]
    elif quota == 'Sleeper':
        response = requests.get('http://indianrailapi.com/api/v2/TrainFare/apikey/f0b655638770e7ffc18f1dcef0385648/TrainNumber/12565/From/SEE/To/NDLS/Quota/Sleeper').json()
        f = response["Fares"][3]["Fare"]
    elif quota == 'General':
        response = requests.get('http://indianrailapi.com/api/v2/TrainFare/apikey/f0b655638770e7ffc18f1dcef0385648/TrainNumber/12565/From/SEE/To/NDLS/Quota/General').json()
        f = response["Fares"][4]["Fare"]
    return train(f, action, intent_name)


def location(req, intent_name):
    code = req["queryResult"]["parameters"]["stationcode"]
    action = req["queryResult"]["action"]
    response = requests.get('https://indianrailapi.com/api/v2/StationLocationOnMap/apikey/f0b655638770e7ffc18f1dcef0385648/StationCode/'+code).json()
    link = response["URL"]
    return loc_link(action, link, intent_name)


def src_dest(req, intent_name):
    train_no = req["queryResult"]["parameters"]["train_no"]
    action = req["queryResult"]["action"]
    response = requests.get('https://indianrailapi.com/api/v2/AutoCompleteTrainInformation/apikey/f0b655638770e7ffc18f1dcef0385648/TrainNumberOrName/'+train_no).json()
    source = response["Trains"][0]["Source"]["Code"]
    sarrival=response["Trains"][0]["Source"]["Arrival"]
    dest = response["Trains"][0]["Destination"]["Code"]
    darrival = response["Trains"][0]["Destination"]["Arrival"]
    return src(source, sarrival, dest, darrival, action, intent_name)


def train(f, action, intent_name):
    if action == "TextResponse" and intent_name == 'fare':
        return {

            "fulfillmentText": "The fare is "+str(f)
        }


def loc_link(action, link, intent_name):
    if action == "TextResponse" and intent_name == "location":
        return {
            "fulfillmentText": "Google maps link "+link
        }


def src(source, sarrival, dest, darrival, action, intent_name):
    if action == 'TextResponse' and intent_name == 'sourcedest':
        return{
            "fulfillmentText": "Source: "+source+"Arrival at source: "+sarrival+"Destination: "+dest+"Arrival at destination: "+darrival
        }


if __name__ == '__main__':
    app.run(port=5000, debug=True)