import ntplib
from time import ctime

# This script is used to synchronize every nodes in time, it must be executed for every node

### CONFIGURATION

# Start the server (node)

NTP_SERVER = "127.0.0.1"  # NTP local server adress

### Script

def get_ntp_time():
    """Take the server's hour"""
    client = ntplib.NTPClient()
    try:
        response = client.request(NTP_SERVER)
        print("NTP Time:", ctime(response.tx_time))
    except Exception as e:
        print("Error during time recuperation", e)

### Main function : execution of the script

if __name__ == "__main__":
    get_ntp_time()

# if hour need to be corrected :

"""sudo server makestep""" # server depends of server like chrony or NTPd
