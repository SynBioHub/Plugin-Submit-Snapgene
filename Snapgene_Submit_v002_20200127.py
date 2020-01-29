# -*- coding: utf-8 -*-
"""
Created on Tue Oct 22 18:46:41 2019

@author: JVM
"""
#converter api help http://synbiodex.github.io/SBOL-Validator/?javascript#introduction

import requests, tempfile, os

def DNA_to_GeneBank(filename, partname):    
    newfile_url = "http://song.ece.utah.edu/examples/pages/acceptNewFile.php"
   
    temp = tempfile.NamedTemporaryFile(suffix=".dna")
    get_url = "http://song.ece.utah.edu/dnafiles/" + os.path.basename(temp.name)[:-4]
    partfile = requests.get(filename).content

    temp.write(partfile)
    temp.flush()
    temp.seek(0)

    files = {'fileToUpload': temp}
    
    #upload file
    res = requests.post(newfile_url, files=files,
                      headers = {"Accept":"text/plain"})
    print(res)
    temp.close()

    
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

   
    content = resp.json()
    return content["result"]

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#FLASK_APP=app.py flask run
from flask import Flask, request, abort
#from Full_v004_20190506 import *
app = Flask(__name__)

#flask run --host=0.0.0.0
@app.route("/dnasubmit/status")
def imdoingfine():
    return("Not dead Jet")


@app.route("/dnasubmit/evaluate", methods=["POST"])
def evaluate():
    return("Accepting Everything")   


@app.route("/dnasubmit/run", methods=["POST"])
def wrapper():
    data = request.json
    files = data['manifest']['files']

    for file in files:
        try:
            url = file['url']
            partname = file['filename']
            sbolcontent = DNA_to_GeneBank(url, partname)
            return sbolcontent
        except Exception as e:
            print(e)
            abort(404)
