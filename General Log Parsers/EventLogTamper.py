import os
import csv
from datetime import datetime
from evtx import PyEvtxParser

# Define the event IDs for Security and System logs for potential tampering events
security_event_ids = {1102, 4719}
system_event_ids = {104}

# Output directories for Security and System logs
output_directory = os.path.join(os.path.expanduser("~"), 'Desktop', 'CLaPT_Output')
security_output_directory = os.path.join(output_directory, 'Security')
system_output_directory = os.path.join(output_directory, 'System')

# Create output directories if they don't exist
os.makedirs(security_output_directory, exist_ok=True)
os.makedirs(system_output_directory, exist_ok=True)

def parse_events(log_path, event_ids):
    events = []
    log = PyEvtxParser(log_path)
    for record in log.records():
        event_id = record.get('EventID')
        if event_id is not None and event_id in event_ids:
            events.append(record)
    return events


def process_and_save_to_csv(events, output_directory, csv_filename, headers):
    if not events:
        print(f"No potential tampering events found in {csv_filename.split('_')[-1].replace('.csv', '')} log.")
    else:
        print(f"Potential Tampering Events in {csv_filename.split('_')[-1].replace('.csv', '')} Log:")
        print("-/-/-/-/-/-/-/-/-/-/-/-/")

        with open(os.path.join(output_directory, csv_filename), 'w', newline='') as csv_file:
            csv_writer = csv.DictWriter(csv_file, fieldnames=headers)
            csv_writer.writeheader()
            for event in events:
                time_created = datetime.fromtimestamp(event['EventTime'] / 1e7 - 11644473600)
                csv_writer.writerow({'Time': time_created, 'EventID': event['EventID'], 'EventData': event['EventData']})
                print(f"Time: {time_created}")
                print(f"Event ID: {event['EventID']}")
                print(f"Event Data: {event['EventData']}")
                print("-/-/-/-/-/-/-/-/-/-/-/-/")

        print(f"Potential tampering events have been processed and saved to {csv_filename}.")

# Process and save Security log
security_log_path = os.path.join(os.environ['SystemRoot'], 'System32', 'winevt', 'Logs', 'Security.evtx')
security_events = parse_events(security_log_path, security_event_ids)
security_csv_filename = 'Potential_Tampering_Events_Security.csv'
process_and_save_to_csv(security_events, security_output_directory, security_csv_filename, ['Time', 'EventID', 'EventData'])

# Process and save System log
system_log_path = os.path.join(os.environ['SystemRoot'], 'System32', 'winevt', 'Logs', 'System.evtx')
system_events = parse_events(system_log_path, system_event_ids)
system_csv_filename = 'Potential_Tampering_Events_System.csv'
process_and_save_to_csv(system_events, system_output_directory, system_csv_filename, ['Time', 'EventID', 'EventData'])
