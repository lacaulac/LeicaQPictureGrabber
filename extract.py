import requests
import sys
import os

def test404AtIPPort(ip, port):
    # Just check if the request at the root path returns a 404
    try:
        return requests.get("http://"+str(ip)+":"+str(port)+"/", timeout=1).status_code == 404
    except Exception:
        return False

CameraIP = "192.168.54.1"

if len(sys.argv) != 2:
    print("Usage: python extract.py IPADDRESS/scan")
    exit()
if sys.argv[1] == "scan":
    import netifaces
    import ipaddress
    base = netifaces.ifaddresses(netifaces.gateways()['default'][netifaces.AF_INET][1])[netifaces.AF_INET][0]
    print("Looking for the camera...")
    hasFoundCamera = False
    for host in ipaddress.IPv4Interface(base['addr']+"/"+base['netmask']).network.hosts():
        #print("Testing %s" % str(host))
        if test404AtIPPort(host, 50001) and test404AtIPPort(host, 60606):
            CameraIP = str(host)
            print("Found the camera at IP " + str(host))
            hasFoundCamera = True
            break
        #Do smth
    if not hasFoundCamera:
        print("Couldn't find the camera...")
        exit()
else:
    CameraIP = sys.argv[1]

startURL = "http://" + CameraIP
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
    #print("Current assoc size : %d" % len(assoc.keys()))
    print("Requesting metadata for %d pictures starting at index %d."%(finish, start))
    result = requests.post(startURL + portThing + SOAPInterface, data=getRangeReqString(start, finish), headers=headers, timeout=20)
    #print(result.content)
    oldAssocSize = len(assoc.keys())

    arr = (str(result.content)).split(startURL)
    for elem in arr:
        if "DT" in elem:
            elem = startURL + (elem.split(".JPG")[0]) + ".JPG"
            assoc[elem] = elem.replace("DT", "DO")

    return len(assoc.keys()) - oldAssocSize

if not os.path.exists("pictures"):
    os.mkdir("pictures")
    print("Created the pictures folder !")

print("Identifying available files...")

while doRange(currentStart, step) == step:
    currentStart += step

#print("Current assoc size : %d" % len(assoc.keys()))

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