#performing flask imports

from flask import Flask, jsonify, request, render_template 
import json
import PyPDF2
from werkzeug.serving import WSGIRequestHandler
import requests
import os
import git




response=""

app = Flask(__name__) 


@app.route('/git_update', methods=['POST'])
def git_update():
    repo = git.Repo('./SRbackend')
    origin = repo.remotes.origin
    repo.create_head('main',
                     origin.refs.main).set_tracking_branch(origin.refs.main).checkout()
    origin.pull()
    return ''

@app.route('/pdftotxt', methods = ['GET',"POST"])
def pdftotxt():
    global response
    global r
    global x
    if(request.method=="POST"):
        
        request_data = request.data
        request_data = json.loads(request_data.decode("utf-8"))
        url = request_data["Download_link"]
        filename = request_data["filename"]
        r = requests.get(url, allow_redirects=True, timeout=20)

        result = open(filename, 'wb').write(r.content)
    
        pdfReader = PyPDF2.PdfFileReader(filename, strict=False)
 
        print(" No. Of Pages :", pdfReader.numPages)
        x=0
        list=[]


        for i in range (0, pdfReader.numPages):
  
            pageObject = pdfReader.getPage(x)
 
            page = pageObject.extractText()
            list.append(page)

            x=x+1

        newline = '\n'.join([str(elem) for elem in list])  
        initialresult = newline.replace("\n"," ")
        result=initialresult.replace("!", "! ")
        initialresponse= result.replace("  ", " ")
        response = initialresponse.replace("  ", " ")
     
        os.remove(filename)  
    
 
        return " "

    else: return jsonify({"file": response})    


        

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    WSGIRequestHandler.protocol_version = "HTTP/1.1"
    app.run(debug = False, host="0.0.0.0", port=5000) 