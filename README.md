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
* Run `install -r requirements.txt`.
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
* Python 3.x
* Flask
* npm
* reactjs
* react-bootstrap
* babelify
* browserify
* 
