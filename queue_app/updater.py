# import paramiko
import json
import time
import subprocess
from . import app

def update_printer():
    # Initialize Paramiko, get information from config file
    # ssh = paramiko.SSHClient()
    # ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # ssh.connect(app.config['SSH_SERVER'], username = app.config['SSH_USERNAME'], password = app.config['SSH_PASSWORD'])
    
    # Get the initial printer data from "printers_init.json"
    with open('queue_app/static/json/printers_init.json', 'r') as json_printer:
        printer_data = json.load(json_printer)
    
    for printer in printer_data['printers']:
        # stdin, stdout, stderr = ssh.exec_command("lpq -P" + printer['name'])
        proc = subprocess.Popen(["rlpq", "-N", "-H", app.config['SERVER'], "-P" + printer['name']], stdout=subprocess.PIPE).communicate()[0]
        output = proc.decode('utf-8').split('\n')
 
        # State Guide:
        # 1 - No Entries
        # 2 - Operating
        # 3 - Warning
        # 4 - Fatal Errors
        # Honestly this is just a handful of output that the printer can give you.
        # We just target the most common output.

        if len(output) == 1:
            if 'no entries' in output[0].lower():
                printer['state'] = 1
            elif 'printer not found' in output[0].lower():
                printer['state'] = 4
                printer['error'] = "The printer is currently not available."

        elif len(output) >= 1:
            # Busy = it's printing
            if 'status: busy' in output[0].lower():
                printer['state'] = 2
            elif 'printerror: check printer' in output[0].lower():
                printer['state'] = 3
                printer['error'] = "The printer is not printing."
            elif 'problems finding printer' in output[0].lower():
                printer['state'] = 3
                printer['error'] = "The printer is experiencing network problems."
            elif 'is down:' in output[0].lower():
                printer['state'] = 4
                printer['error'] = "The printer is down."
            else:
                printer['state'] = 2
            parse_output(printer, output)

        else:
            printer['state'] = 4
            printer['error'] = "Printer did not respond."

    # Command to clean some cache file that appear after running "lpq"
    # ssh.exec_command("lpq-pqtest --kdest")  
    # ssh.close()

    # Update the timestamp
    printer_data['last_updated'] = time.strftime("%a, %b %d, %I:%M %p")

    # Dump all the data into a new JSON file named "printers_data.json"
    with open('queue_app/static/json/printers_data.json', 'w') as write_printer:
        json.dump(printer_data, write_printer, indent=4, sort_keys=True)

    json_printer.close()

def parse_output(printer, output):
    # Find the index where the jobs actually start to be listed
    jobs = ''
    for i, line in enumerate(output):
        if line.lower().split() == ['rank', 'owner', 'job', 'files', 'total', 'size']:
            j = i + 1
            jobs = output[j:]

    # Can't find the list to parse, stop parsing
    if jobs == '':
        return

    queue = []
    for job in jobs:
        info = job.split()
        queue.append({ 'queue_pos':info[0],'user_id':info[1],'job_num':info[2],'filename':''.join(info[3:-2]) })

    printer['queue'] = queue


