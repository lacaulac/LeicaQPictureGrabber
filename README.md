# LeicaQPictureGrabber

A simple python script that allows you to use a Leica Q's Wi-Fi interface to retrieve the pictures you've taken without going through the hassle of moving the memory card. Phones can use Leica's mobile app, why can't computers ?

# Disclaimer

I am not affiliated, associated, authorized, endorsed by, or in any way officially connected with Leica Camera AG or Panasonic Corporation, or any of their subsidiaries or their affiliates. No software analysis had to be done on the mobile applications published by Leica Camera. All my research work was solely based on analysing network frames (hi SSDP/UPnP) and other open-source projects that approached controlling such cameras through their HTTP interfaces.

Please don't sue me <3

# Compatibility

While doing preliminary research, I noticed that the Leica Q shares a lot of software similarities (the http-based command interface being the main one) with other cameras such as Panasonic Lumix cameras (not quite sure about the exact names). I don't have access to any of those cameras so I can't test this out, but I'd really like to have feedback if this works or not!

This might also work with other Leica cameras that are supported by their mobile app, but again, I can't really verify this.

# Usage

## Installation

```bash
# Clone the repo
git clone https://github.com/lacaulac/LeicaQPictureGrabber.git
cd LeicaQPictureGrabber
# Install the requirements
# This is not required if you already know the camera's IP address on your network
pip install -r requirements.txt
```

## Using the thingy

If you know the target IP address (which should be 192.168.54.1 on the self-hosted Wi-Fi), you can just type :
```bash
python extract.py TYPE.IP.ADDRESS.HERE
```

If you're not quite sure what the camera's IP is, you can use an experimental (and badly implemented, if at all) network scanning feature :
```bash
python extract.py scan
```

This feature requires you to install the netifaces python module, which is part of the requirements.

All the cameras's contents will be downloaded in a pictures folder, created in the running directory.

## Known problems

### Videos

Images and videos aren't differentiated yet. The only way to differentiate them at the moment is seeing the .JPG file's preview to be incorrect and realising its size doesn't really match with its supposed format.

### Wi-Fi speed

tl;dr: The wi-fi antenna on the Leica Q (at least the one I'm working with) seems to be quite weak. I'd recommend placing the camera close to the Wi-Fi access point or running a script on a laptop that is connected to the camera self-hosted Wi-Fi hotspot.

After some time spent trying to understand why I was having a hard time testing the script on my desktop computer, I noticed that while my computer was connected using an Ethernet cable, the camera was quite far from the Wi-Fi hotspot. This problem didn't occur when I was testing on a laptop that was connected to the the self-hosted camera Wi-Fi hotspot. I figured this is is due to a "weak" Wi-Fi antenna / amplification circuit, but I could be wrong.

### Battery levels

For reasons unknown accessing the camera's HTTP interfaces works way more reliably when using completely charged batteries. I've noticed requests going unanswered or loading times being extremely slow with low battery levels.