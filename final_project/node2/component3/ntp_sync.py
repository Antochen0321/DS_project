import ntplib
import time
import subprocess
import sys
import os
from time import ctime
from datetime import datetime

# This script is used to synchronize every node in time, it must be executed for every node

### CONFIGURATION

# Start the server (node)
NTP_SERVER = os.getenv("NTP_SERVER", "pool.ntp.org")  # Public NTP server address

# Time difference threshold (in seconds) to trigger correction
TIME_THRESHOLD = 5  # seconds

### SCRIPT

def get_ntp_time():
    """Retrieve the server's hour"""
    client = ntplib.NTPClient()
    try:
        response = client.request(NTP_SERVER)
        current_time = ctime(response.tx_time)
        print("NTP Time:", current_time)
        return response.tx_time  # Return as timestamp for easy comparison
    except Exception as e:
        print("Error during time retrieval:", e)
        return None

def get_system_time():
    """Get the local system time as timestamp"""
    return time.time()

def correct_time():
    """Force the correction of system time using NTP"""
    try:
        print("Attempting to correct time...")
        # subprocess.run(["sudo", "systemctl", "restart", "ntp"], check=True) 
        # if using/don't chrony, comment/uncomment the line above and uncomment/comment that one :
        subprocess.run(["sudo", "chronyc", "makestep"], check=True)
        print("Time corrected successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error correcting time: {e}")
        sys.exit(1)

def main():
    print("--- NTP Time Sync ---")
    
    # Retrieve NTP time
    ntp_time = get_ntp_time()
    
    if ntp_time is None:
        print("Unable to retrieve time from NTP server.")
        sys.exit(1)

    # Get the current system time
    system_time = get_system_time()

    # Calculate the time difference
    time_diff = abs(ntp_time - system_time)

    print(f"Time difference: {time_diff} seconds.")

    # Only correct the time if the difference is above the threshold
    if time_diff > TIME_THRESHOLD:
        print(f"Time difference is greater than {TIME_THRESHOLD} seconds. Applying correction...")
        correct_time()
    else:
        print(f"Time is within acceptable range. No correction needed.")

# Execution of main function
if __name__ == "__main__":
    main()
