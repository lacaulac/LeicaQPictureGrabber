import requests
import sys
import os

startURL = "http://192.168.54.1"
portThing = ":60606/"
SOAPInterface = "Server0/CDS_control"
headers = { 'Content-Type': 'text/xml; charset=utf-8'
          , 'SOAPACTION': 'urn:schemas-upnp-org:service:ContentDirectory:1#Browse'
          }
step = 15
currentStart = 0

def getRangeReqString(StartingIndex, RequestedCount, ObjectID=0):
    return ('''<?xml version="1.0" encoding="utf-8"?>
<s:Envelope s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/" xmlns:s="http://schemas.xmlsoap.org/soap/envelope/">
   <s:Body>
      <u:Browse xmlns:u="urn:schemas-upnp-org:service:ContentDirectory:1">
         <ObjectID>%d</ObjectID>
         <BrowseFlag>BrowseDirectChildren</BrowseFlag>
         <Filter>*</Filter>
         <StartingIndex>%d</StartingIndex>
         <RequestedCount>%d</RequestedCount>
         <SortCriteria />
      </u:Browse>
   </s:Body>
</s:Envelope>''' % (ObjectID, StartingIndex, RequestedCount))

assoc = dict()

def doRange(start, finish):
    print("Current assoc size : %d" % len(assoc.keys()))
    print("Extracting %d pictures starting at %d."%(finish, start))
    result = requests.post(startURL + portThing + SOAPInterface, data=getRangeReqString(start, finish), headers=headers)
    #print(result.content)
    oldAssocSize = len(assoc.keys())

    arr = (str(result.content)).split(startURL)
    for elem in arr:
        if "DT" in elem:
            elem = startURL + (elem.split(".JPG")[0]) + ".JPG"
            assoc[elem] = elem.replace("DT", "DO")

    return len(assoc.keys()) - oldAssocSize

while doRange(currentStart, step) == step:
    currentStart += step

print("Current assoc size : %d" % len(assoc.keys()))

print("Retrieved URLs leading to %d pics" % len(assoc.keys()))

toDownload = dict()

print("Now counting missing files...")
for key in assoc.keys():
    urlSplit = assoc[key].split("/")
    finalFileName = urlSplit[len(urlSplit) - 1]
    if not os.path.exists("pictures/" + finalFileName):
        toDownload[finalFileName] = assoc[key]

print("Done! About to download %d pictures..." % len(toDownload.keys()))

i = 1
for key in toDownload.keys():
    print("[%d/%d]Downloading %s" % (i, len(toDownload.keys()), key))
    imgRes = requests.get(toDownload[key])
    with open("pictures/"+key, "wb") as imgFl:
        imgFl.write(imgRes.content)
    i += 1

with open("result.html", "w") as fl:
    fl.write("<html><head><title>Hello !</title></head><body>")
    for keys in assoc.keys():
        fl.write('<a href="%s"><img src="%s"></a><br>' % (assoc[keys], keys))

    fl.write("</body></html>")

with open("entries.txt", "w") as fl:
    for keys in assoc.keys():
        fl.write("%s\n" % assoc[keys])