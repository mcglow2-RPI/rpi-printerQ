# rpi-printerQ

A complete rewrite of TrevorNT's [RPI PrinterQueue-NG](https://github.com/TrevorNT/rpi-printqueue-ng). The old version of the printer queue had a tendency to crash once in a while and unnecessarily used a database to store printer data.

## Changes
* Flask instead of Django
* Usage of ReactJS on the frontend to avoid page refreshing to re-render data
* Data is stored in a single JSON file rather than a database

## Getting Started
### Requirements
* Python 3.x
* Flask

### Installation
* **Recommended:** Setup a virtualenv.
* Run `pip install -r requirements.txt`.
* [Setup your config file](https://github.com/albshin/rpi-printerQ#config-file).
* Run `python app.py`.
* Go to [http://localhost:5000/](http://localhost:5000/).

#### Config File
**Example:**
```
SSH_SERVER = 'this-server.edu'
SSH_USERNAME = 'anon'
SSH_PASSWORD = 'hunter2'
```

## Development
### Dependencies
* **Python 3.x** - For Flask
* ~ **Paramiko** - SSH capabilities
* ~ **APScheduler** - Calling the updater every set interval
* ~ **Flask** - Serving webpages, running SSH commands to the printers, storing data
* **npm** - Frontend package manager
* **reactjs** - Displaying and updating data from Flask
* **react-bootstrap** - Styling
* **babelify** - For use with ReactJS + Browserify
* **browserify** - Packaging node modules and ReactJS code into a single JS file

### File Structure
```
.
├── queue_app               # Flask application files
│   ├── static              # Location of all CSS/JS/JSON/Fonts files
│   ├── templates           # Location of all HTML files
│   ├── __init__.py         # Main Flask applicaton file. Routes and auto-updater are defined here  
│   └── updater.py          # Code for updater
├── app.py                  # Python file to run Flask application
├── config.py               # Config file that stores server/user account information
├── main.js                 # Source code for ReactJS
├── requirements.txt
├── package.json
└── README.md
```
