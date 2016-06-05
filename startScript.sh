#!/bin/sh
# Sleep for 30 seconds, to wait for NETWORK IP
# should remove this or make it small once the threading part is done
sleep 30

#run the piMon.py python script
sudo ./home/pi/piMon/piMon.py

# Edit the etc/rc.local and add these lines at END before exit 0
# /home/pi/piMon/startScript.sh &
