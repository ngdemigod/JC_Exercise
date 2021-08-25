from flask import Flask, render_template, request
import flask
import os, requests



#Global Variables
dir = os.getcwd()
dFolder = dir + "/downloads/sample.txt"
testURL = "https://www.learningcontainer.com/wp-content/uploads/2020/04/sample-text-file.txt"


# Function: Download file from URL 
def dFuction():
    dRequest = requests.get(testURL)
    dFile = open(dFolder, 'w').write(dRequest.text)
    return


#Using Flask to create app
app = Flask(__name__)

#Route to home page
@app.route('/', methods=['GET'])
def home():
    return render_template("home.html")


#Route to /manage_file endpoint
@app.route('/manage_file', methods=['POST'])
def mfile():
    jres = {}
    content = []
    
    try:
        payload = request.get_json() #loads the api request into the payload variable
    except:
        loadError = "JSON request payload failed to load correctly"
        jres['error'] = loadError 
        return flask.jsonify(jres), 500
    


# Based on JSON payload, the app will run a function
    if payload["action"] == "download":
        try:
            dFuction()
            if os.path.isfile(dFolder): jres['success'] = True
            return flask.jsonify(jres), 200
        except:
            loadError = "Failed to perform download operation"
            jres['error'] = loadError 
            return flask.jsonify(jres), 500

    elif payload['action'] == 'read':
        try:
            if os.path.isfile(dFolder):
                rFile = open(dFolder, 'r').read()
                content.append(rFile)
        
            else:
                dFuction()
                rFile = open(dFolder, 'r').read()
                content.append(rFile)

        except:
            loadError = "Failed to perform read operation"
            jres['error'] = loadError 
            return flask.jsonify(jres), 500

        if content: jres['read'] = content
        content=[]
        jres['success'] = True

        return flask.jsonify(jres), 200     

if __name__ == '__main__':
    app.run(debug=True)


