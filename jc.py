from flask import Flask, render_template, request
import flask
import os, requests, signal
from datetime import date
from logs.log import logger

### Global Variables ###
dir = os.getcwd() #return app directory
dFolder = dir + "/downloads/sample.txt" # path to the downloaded file
testURL = "https://www.learningcontainer.com/wp-content/uploads/2020/04/sample-text-file.txt" #URL of file to be downloaded


### Custom Logging ###
logging = logger('Other')

### Function: Download file from URL ###
def dFuction():
    dRequest = requests.get(testURL)
    dFile = open(dFolder, 'w').write(dRequest.text)
    return

logging.info("Starting application")

### Using Flask to create app ###

app = Flask(__name__)

# Route to home page
@app.route('/', methods=['GET'])
def home():
    logging.info("Routing to homepage at /")
    return render_template("home.html")


# Route to /manage_file endpoint
@app.route('/manage_file', methods=['POST'])
def mfile():
    logging.info("Routing POST at /manage_file")
    jres = {}
    content = []
    
    try:
        payload = request.get_json() #loads the api JSON request into the payload variable
    except:
        loadError = "JSON request payload failed to load correctly"
        logging.error(loadError)
        jres['error'] = loadError 
        return flask.jsonify(jres), 500
    else:
        logging.info(f"JSON payload received. {payload}")
    

### Based on JSON payload, the app will run a function
# Executing Download operation
    if payload["action"] == "download":
        logging.info("Attempting download operation")
        try:
            dFuction()
            if os.path.isfile(dFolder): 
                jres['success'] = True
                logging.info(f"File successfully saved at {dFolder}")
            return flask.jsonify(jres), 200
        except:
            loadError = "Failed to perform download operation"
            logging.error(loadError)
            jres['error'] = loadError 
            return flask.jsonify(jres), 500

# Executing Read operation            
    elif payload['action'] == 'read':
        logging.info("Attempting read operation")
        try:
            if os.path.isfile(dFolder):
                logging.info("File detected, attempting to read")
                rFile = open(dFolder, 'r').read()
                content.append(rFile)
        
            else:
                logging.warning("File not found. Attempting to download and re-run read operation")
                dFuction()
                rFile = open(dFolder, 'r').read()
                content.append(rFile)

        except:
            loadError = "Failed to perform read operation"
            logging.error(loadError)
            jres['error'] = loadError 
            return flask.jsonify(jres), 500

        if content: jres['read'] = content
        logging.info("Successfully executed read operation")
        content=[]
        jres['success'] = True
        return flask.jsonify(jres), 200     



#### Shutdown the application ###
def shutdown(sd = False):
    logging.warning("Attempting to shutdown the application")
    if sd:
        logging.info("Application shutdown executed")
    else:
        logging.error("Application failed to shutdown") 

def sd_handler(signum, frame):
    shutdown(sd = True)

signal.signal(signal.SIGINT, sd_handler) # shuts down application when Ctrl+C is entered


if __name__ == '__main__':
    app.run(debug=True)


