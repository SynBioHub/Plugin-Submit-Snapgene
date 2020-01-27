# -*- coding: utf-8 -*-
"""
Created on Tue Oct 22 18:46:41 2019

@author: JVM
"""
#converter api help http://synbiodex.github.io/SBOL-Validator/?javascript#introduction

import requests

def DNA_to_GeneBank(filename, partname):    
    newfile_url = "http://song.ece.utah.edu/examples/pages/acceptNewFile.php"
    

#    #find partname
#    a = filename.find('.')
#    b = filename.rfind('\\')
#    
#    if b<0:
#        b = 0
#    partname = filename[b+1:a]
    
    get_url = "http://song.ece.utah.edu/dnafiles/"+partname
    
    #linearity and detectFeatures works on presence so set those parameters
    data = {}
    
    #file to open
    partfile = requests.get(filename).text

#    partfile = open(filename ,"rb")
    files = {'fileToUpload': partfile}
    
    #parameters
    params = {} 
    
    #upload file
    requests.post(newfile_url, files=files, data = data, params = params,
                      headers = {"Accept":"text/plain"})
    #close file
    partfile.close()
    
    #request genebank
    s = requests.get(f"{get_url}.gb")
    genebank = s.text
    
    
    request = { 'options': {'language' : 'SBOL2',
                            'test_equality': False,
                            'check_uri_compliance': False,
                            'check_completeness': False,
                            'check_best_practices': False,
                            'fail_on_first_error': False,
                            'provide_detailed_stack_trace': False,
                            'uri_prefix': 'trial',
                            'version': '',
                            'insert_type': False
                                    },
                'return_file': True,
                'main_file': genebank
              }
    
    resp = requests.post("https://validator.sbolstandard.org/validate/", json=request)

    content = resp.text
    start = content.find("result")
    content2 = content[start+9:]
    end = content2.rfind(">")
    content2 = content2[:end+1]
    content2 = content2.replace("\\n", "\n")
    
    with open(filename[:-4]+"_SBOL.rdf", 'w') as f:
        f.write(content2)

    return(content2)

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#FLASK_APP=app.py flask run
from flask import Flask, request, abort
#from Full_v004_20190506 import *
app = Flask(__name__)

#flask run --host=0.0.0.0
@app.route("/dnasubmit/status")
def imdoingfine():
    return("Not dead Jet")


@app.route("/dnasubmit/evaluate")
def evaluate():
    return("Accepting Everything")   


@app.route("/dnasubmit/run", methods=["POST"])
def wrapper():
    data = request.json
    for file in data:
        try:
            #instance = "synbiohub.org"
            url = file['url']
            partname = file['name']
            print(url)
            sbolcontent = DNA_to_GeneBank(url, partname)
            return sbolcontent
        except Exception as e:
            print(e)
            abort(404)

