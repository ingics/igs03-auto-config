# igs03-auto-config
Example of iGS03E auto configuration by Multicast DNS Service Discovery.

## Setup
Install required packages
```
pip install -r requirements.txt
```

## Usage

Execute the autoconfig.py
```
python autoconfig.py
```

Power on and plug iGS03E on the same network.
The script should find the new appear iGS03E device and try to config it through telenet.

Example output, it found two iGS03E and check the HTTP CN_CHECK setting.
```
[2021-04-01 10:06:09,861] INFO - Found IGS03E-v1.0.5.0 [10:52:1C:89:C2:07]._ble-gw._tcp.local. at 192.168.1.109
[2021-04-01 10:06:09,861] INFO - Connecting, try 1 ...
[2021-04-01 10:06:09,865] INFO - Login as admin, admin
[2021-04-01 10:06:09,875] INFO - Logged in ...
[2021-04-01 10:06:09,924] INFO - Get HTTP CN_CHECK = 1
[2021-04-01 10:06:09,925] INFO - Found IGS03E-v1.0.5.0 [F0:08:D1:6C:A8:17]._ble-gw._tcp.local. at 192.168.1.104
[2021-04-01 10:06:09,925] INFO - Connecting, try 1 ...
[2021-04-01 10:06:09,932] INFO - Login as admin, admin
[2021-04-01 10:06:09,961] INFO - Logged in ...
[2021-04-01 10:06:10,015] INFO - Get HTTP CN_CHECK = 1
```

And you can modify the autoconfig.py for your own setting requiremenet.

### Notice

The scripts been tested on Ubuntu 20.04 with Python 3.8.
