import json
import logging
import re
import subprocess
from datetime import datetime

adb_file_path = "/Users/user/PycharmProjects/AppiumAutomation/ADB_logs.json"

iteration_failed_to_launch = "iteration_failed_to_launch: True"

ble_start_conn = 'Connecting to device: BXE604'
ble_end_conn = 'Device is fully connected: DeviceEntry: UUID='
ble_failed_conn = 'Failed to locate device'

def search_file(filename, keyword, ble_start_stop, context_lines=0):
    try:
        # Open the file for reading
        with open(filename, 'r') as file:
            # Iterate over each line of the file
            for line in file:

                # Strip newline characters and check if the line contains the keyword
                if keyword in line.strip():
                    print(line.strip())
                    timestamp_pattern = r'\d{2}:\d{2}:\d{2}\.\d{3}'
                    match = re.search(timestamp_pattern, line)
                    if match:
                        print(f"{ble_start_stop} is: {match.group(0)}")
                        match_int = datetime.strptime(str(match.group(0)), '%H:%M:%S.%f')
                        hours = match_int.hour
                        minutes = match_int.minute
                        seconds = match_int.second
                        microseconds = match_int.microsecond
                        total_seconds = (hours * 3600) + (minutes * 60) + seconds + (microseconds / 1e6)
                        print(f"____total seconds:{total_seconds}")
                        return total_seconds
                    else:
                        return None

            print(f"no required keyword: '{keyword}' found in the log")
            return None
    except FileNotFoundError as fileNotFoundError:
        print(f"<{fileNotFoundError}>Error: File '{filename}' not found.")
    except TypeError as typeError:
        print(f"here is an ERROR{typeError}")



ble_conn_start_time = search_file(adb_file_path, ble_start_conn, ble_start_stop="START time", context_lines=0)
ble_conn_end_time = search_file(adb_file_path, ble_end_conn, ble_start_stop="STOP time", context_lines=0)
ble_failed_conn_time = search_file(adb_file_path, ble_failed_conn, ble_start_stop=ble_failed_conn, context_lines=0)


if ble_conn_start_time is not None and ble_conn_end_time is not None:
    ble_start_to_success_connect_duration = round(ble_conn_end_time - ble_conn_start_time, 2)
elif ble_conn_start_time is not None and ble_failed_conn_time is not None:
    ble_start_to_failed_connect_duration = round(ble_failed_conn_time - ble_conn_start_time, 2)
else:
    print(iteration_failed_to_launch)


def json_data_dump_file(json_file_path):

    new_data = {
        #"ble_start_conn": ble_conn_start_time,

        # "ble_end_conn": conn_end_time,
        # "ble_start_to_connect_duration": ble_start_to_connect_duration,
        # "ble_failed_conn": ble_failed_conn
    }

    if ble_start_to_success_connect_duration:
        new_data.update({"ble_start_conn": ble_conn_start_time})
        new_data.update({"ble_conn_end_time": ble_conn_end_time})
        new_data.update({"ble_start_to_connect_duration": ble_start_to_success_connect_duration})
    elif ble_start_to_failed_connect_duration:
        new_data.update({"ble_start_conn": ble_conn_start_time})
        new_data.update({"ble_failed_conn_time": ble_failed_conn_time})
        new_data.update({"ble_start_to_connect_duration": ble_start_to_failed_connect_duration})
    else:
        logging.info("iteration_failed_to_launch")
        new_data.update({"iteration_failed_to_launch": iteration_failed_to_launch})

    json_file_path = f"{json_file_path}"


    # Read existing data from the JSON file, if it exists
    try:
        with open(json_file_path, 'r') as json_file:
            existing_data = json.load(json_file)
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        # If the file doesn't exist, initialize with an empty dictionary
        existing_data = []
    existing_data.append(new_data)
    # Write the updated data back to the JSON file
    with open(json_file_path, 'w') as json_file:
        json.dump(existing_data, json_file, indent=4)

    print(f"{new_data} has been dumped into '{json_file_path}'")




json_data_dump_file("/Users/user/PycharmProjects/AppiumAutomation/test_data.json")












# def search_logs(keyword, context_lines=0):
#     # Run adb logcat command
#     process = subprocess.Popen(['adb', 'logcat'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#
#     # Iterate over each line of the output
#     for line in iter(process.stdout.readline, b''):
#         # Decode the line from bytes to string
#         line = line.decode('utf-8').strip()
#         # Check if the line contains the keyword
#         if keyword in line:
#             # Print the line
#             print(line)
#             # Print context lines if specified
#             if context_lines > 0:
#                 for _ in range(context_lines):
#                     prev_line = process.stdout.readline().decode('utf-8').strip()
#                     print(prev_line)
#
# # Example usage: Search for keyword "error" with 2 context lines
# search_logs(ble_start_conn, context_lines=2)
