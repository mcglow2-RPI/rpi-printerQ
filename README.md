# rpi-printerQ

A complete rewrite of TrevorNT's [RPI PrinterQueue-NG](https://github.com/TrevorNT/rpi-printqueue-ng). The old version of the printer queue had a tendency to crash once in a while and unnecessarily used a database to store printer data.

## Changes
* Flask instead of Django
* Usage of ReactJS on the frontend to avoid page refreshing to re-render data
* Data is stored in a single JSON file rather than a database

## Getting Started

### Requirements
* Python 3.x

### Installation
* **Recommended:** Setup a virtualenv.
* Run `install -r requirements.txt`.
* [Setup your config file](docs/README.md/#Config File)
* Run `python app.py`.
* Go to [http://localhost:5000/](http://localhost:5000/).

### Config File
Rename `config.def.py` to `config.py` and fill in the fields with the correct server (omitted to general public), your RCS username, and password.

**Example:**
```
SSH_SERVER = 'this-server.edu'
SSH_USERNAME = 'anon'
SSH_PASSWORD = 'hunter2'
```
