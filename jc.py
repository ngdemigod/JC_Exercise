from flask import Flask, render_template,request
import flask
import requests, os



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
    payload = request.get_json()

    jres = {}
    content = []

    if payload["action"] == "download":
        dFuction()
        if os.path.isfile(dFolder): jres['success'] = True
        return flask.jsonify(jres), 200

    elif payload['action'] == 'read':
        if os.path.isfile(dFolder):
            rFile = open(dFolder, 'r').read()
            content.append(rFile)
            
        else:
            dFuction()
            rFile = open(dFolder, 'r').read()
            content.append(rFile)

        if content: jres['read'] = content
        content=[]
        jres['success'] = True

        return flask.jsonify(jres), 200     

  




if __name__ == '__main__':
    app.run(debug=True)


