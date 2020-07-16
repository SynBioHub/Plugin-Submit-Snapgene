# -*- coding: utf-8 -*-
"""
Created on Tue Oct 22 18:46:41 2019

@author: JVM
"""
#FLASK_APP=app.py flask run
from flask import Flask, request, abort, jsonify, send_file
from DNA_to_GenBank import DNA_to_GenBank
import os, shutil
app = Flask(__name__)

#flask run --host=0.0.0.0
@app.route("/status")
def imdoingfine():
    return("The Snapgene Submit Plugin is up and running")


@app.route("/evaluate", methods=["POST"])
def evaluate():
    #uses MIME types
    #https://developer.mozilla.org/en-US/docs/Web/HTTP/Basics_of_HTTP/MIME_types/Common_types
    
    eval_manifest = request.get_json(force=True)
    files = eval_manifest['manifest']['files']
    
    eval_response_manifest = {"manifest":[]}
    
    for file in files:
        file_name = file['filename']
        file_type = file['type']
        file_url = file['url']
        
        ########## REPLACE THIS SECTION WITH OWN RUN CODE #################
        #Special case as .dna file has no mime type
        file_type = file_name.split('.')[-1]
        
        #types that can be converted to sbol by this plugin
        acceptable_types = {'.dna'}
        
        #types that are useful (will be served to the run endpoint too but noted that they won't be converted)
        useful_types = {}
        
        file_type_acceptable = file_type in acceptable_types
        file_type_useable = file_type in useful_types
        ################## END SECTION ####################################
        
        if file_type_acceptable:
            useableness = 2
        elif file_type_useable:
            useableness = 1
        else:
            useableness = 0
        
        eval_response_manifest["manifest"].append({
            "filename": file_name,
            "requirement": useableness})
       
    return jsonify(eval_response_manifest) 


@app.route("/run", methods=["POST"])
def wrapper():
    cwd = os.getcwd()
    
    zip_path_in = os.path.join(cwd, "To_zip")
    zip_path_out = os.path.join(cwd, "Zip")
    
    #remove to zip directory if it exists
    try:
        shutil.rmtree(zip_path_in, ignore_errors=True)
    except:
        print("No To_zip exists currently")
        
    #make to zip directory
    os.makedirs(zip_path_in)
    
    #take in run manifest
    run_manifest = request.get_json(force=True)
    files = run_manifest['manifest']['files']
    
    #initiate response manifest
    run_response_manifest = {"results":[]}
    
    
    for file in files:
        try:
            file_name = file['filename']
            file_type = file['type']
            file_url = file['url']
            data = str(file)
           
            converted_file_name = f"{file_name}.converted"
            file_path_out = os.path.join(zip_path_in, converted_file_name)
        
            ########## REPLACE THIS SECTION WITH OWN RUN CODE #################
            sbolcontent = DNA_to_GenBank(file_url, file_name)
            return sbolcontent
            ################## END SECTION ####################################
            
            #write out result to "To_zip" file
            with open(file_path_out, 'w') as xmlfile:
                xmlfile.write(sbolcontent)
            
            # add name of converted file to manifest
            run_response_manifest["results"].append({"filename":converted_file_name,
                                        "sources":[file_name]})
            
        except Exception as e:
            print(e)
            abort(415)
            
    #create manifest file
    file_path_out = os.path.join(zip_path_in, "manifest.json")
    with open(file_path_out, 'w') as manifest_file:
            manifest_file.write(str(run_response_manifest)) 
        
    #create zip file of converted files and manifest
    shutil.make_archive(zip_path_out, 'zip', zip_path_in)
    
    #clear To_zip directory
    shutil.rmtree(zip_path_in, ignore_errors=True)
    
    return send_file(f"{zip_path_out}.zip")
    
    #delete zip file
    os.remove(f"{zip_path_out}.zip")