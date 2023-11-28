#! /usr/bin/env python
import requests
import json
import time

ip = "192.168.178.135"
url = f"http://{ip}/http-read.json?encrypted=1"
key = "paste-key-here"
request_timeout = 10
retries = 3
retry_delay = 2
# Base Tumble Dryer status
candyOff = {
    "StatoWiFi": "1",
    "StatoTD": "1",
    "CodiceErrore": "255",
    "Pr": "0",
    "PrPh": "0",
    "RemTime": "0",
    "DryLev": "0",
    "Time": "0",
    "Rapido": "0",
    "Opt1": "0",
    "Opt2": "0",
    "Opt3": "0",
    "Opt4": "0",
    "Opt5": "0",
    "Opt6": "0",
    "Opt7": "0",
    "Opt8": "0",
    "Refresh": "0",
    "CleanFilter": "0",
    "WaterTankFull": "0",
    "DryingManagerLevel": "0",
    "DelVal": "255",
    "DoorState": "None",
    "RecipeId": "0",
    "CheckUpState": "0",
}

tries = 0
candy = {}


# extract data
def fetchHex(xurl, xrequest_timeout):
    try:
        candyhex = requests.get(xurl, timeout=xrequest_timeout).text
        return candyhex
    except Exception:
        return None


# convert data to readable text
def convText():
    hexText = fetchHex(url, request_timeout)
    if hexText is None:
        return None
    bytes_object = bytes.fromhex(hexText)
    coded = bytes_object.decode("ASCII")
    return coded


# decode data
def decode(xkey):
    xored = str()
    codedText = convText()
    if codedText is None:
        return None
    repeated_key = (xkey) * ((len(codedText) // len(xkey)) + 1)
    for x in range(len(codedText)):
        xored += chr(ord(codedText[x]) ^ ord(repeated_key[x]))
    return xored


# strip and print data
while tries < retries:
    decoded = decode(key)
    if decoded is not None:
        decodedDict = json.loads(decoded)
        candyData = decodedDict.get("statusTD")
        for k, v in candyData.items():
            # Exluding some entries from the json got from the TD
            # We need to stay below 255 chars
            if (
                k[0:3] != "Opt"
                and k[0:3] != "Rec"  # e.g. RecipeId
                and k[0:3] != "Ste"
                and k[0:3] != "SLe"
                and k[0:3] != "Che"  # e.g. CheckUpState
                and k != "DryingManagerLevel"
                and k[0:3] != "Ref"  # e.g. RecipeId
                and k[0:3] != "Rap"  # e.g. RecipeId
            ):
                if k == "DelVal" and candyData[k] == "255":
                    candy["DelVal"] = "0"
                else:
                    candy[k] = candyData[k]
        # Creating TotalTime entry that is the estimate cycle time + the delay
        # So you know at what time the clothes are ready
        TotalTime = int(candy["DelVal"]) * 60 + int(candy["RemTime"])
        candy["TotalTime"] = str(TotalTime)
        candyJson = json.dumps(candy, indent=4)
        break
    tries += 1
    time.sleep(retry_delay)
if tries == retries:
    candyJson = json.dumps(candyOff, indent=4)
print(candyJson)
