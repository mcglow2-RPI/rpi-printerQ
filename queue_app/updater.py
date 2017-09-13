import paramiko
import json
import time
import subprocess
import sys
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

        if printer['method'] == 'ssh':
            stdin, stdout, stderr = ssh.exec_command("lpq -P" + printer['name'])
            output = stdout.readlines()
        elif printer['method'] == 'rlpq':
            if 'server' in printer.keys():
                if printer['server'] != '':
                    server = printer['server']
            
            proc = subprocess.check_output(["rlpq", "-H", server, "-P" + printer['name'] , "-N" ], stderr=subprocess.STDOUT)
            output = proc.decode('utf-8').split('\n')

        print "Checking server:" + server + " queue: " +  printer['name']

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
            elif 'Malformed from address' in output[0].lower():
                printer['state'] = 3
                printer['error'] = "Access to print server denied."

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

def parse_output_ssh(printer, output):
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

def parse_output(printer, output):
    if 'Windows LPD Server' in str(output):
        return parse_output_windows(printer, output)
    else:
        return parse_output_rcs(printer, output)


def parse_output_rcs(printer, output):
    print "parsing for RCS format"
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
        if job == '':
            continue
        if job == 'no entries':
            continue

        try:
            #print job
            info = job.split()
            queue.append({'queue_pos': info[0], 'user_id': info[1], 'job_num': info[2], 'filename': ''.join(info[3:-2])})

        except  (RuntimeError, TypeError, NameError, IndexError):
            print "Error with parse: " + job

    printer['queue'] = queue


def parse_output_windows(printer, output):
    print "parsing for Windows LPD format"
    # Find the index where the jobs actually start to be listed
    jobs = ''
    for i, line in enumerate(output):
        if line.lower().split() == ['owner', 'status', 'jobname', 'job-id', 'size', 'pages', 'priority']:
            j = i + 1
            jobs = output[j:]

    # Can't find the list to parse, stop parsing
    if jobs == '':
        return

    queue = []
    count = 1
    for job in jobs:
        if job == '':
            continue
        if job.replace('-','') == '':
            continue
        if job == 'no entries':
            continue
        if job is None:
            continue

        try:
            #print job
            info = job.split()
            queue.append({'queue_pos': count, 'user_id': str(info[0]).lower(), 'job_num': info[3], 'filename': ' '.join(info[2:-4])})
            count = count + 1
        except  (RuntimeError, TypeError, NameError, IndexError):
            print "Error with parse: " + job

    printer['queue'] = queue


