# rpi-printerQ

Tool to list output of Linux rlpq command on a webpage.  Support multiple print queues on different print servers.

* Uses [Flask](http://flask.pocoo.org/) Micro Framework
* Uses ReactJS on the frontend to avoid page refreshing to re-render data
* Queue configuration and job data is stored in JSON files rather than a database

## Getting Started
### Requirements
* Python 3.x
* Flask
* rlpq

### Installation
* **Recommended:** Setup a virtualenv.
* Run `pip install -r requirements.txt`.
* [Setup your config file](https://github.com/albshin/rpi-printerQ#config-file).
* Run `python app.py`.
* Go to [http://localhost:5000/](http://localhost:5000/).

**Permissions:**

*The file queue_app/static/json/printers_data.json needs to be writeable by the account that python and/or your webserver is running as.

#### Config File
**Example:**
```
BASE_PATH='should normally be left blank, but can be set to path to app if relative links to json files dont work'
DEFAULT_LPQ_SERVER = 'main print server to use if not specified per queue'
```

**Allow remote IPs:**

By default the application binds to localhost.  To support connections from remote clients make the following change to app.py from
```
if __name__ == '__main__':
    app.run(debug=True)
```
to
```
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
```

**Print Queues:**
Print queues to monitor are specified in the file queue_app/static/json/printers_init.json

```
{
    "name": "queue name",
    "server": "optional print server hostname",
    "state": 0,
    "error": "",
    "queue": []
},
```

## Development
### Dependencies
* **Python 3.x** - For Flask
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
