# -*- coding: utf-8 -*-
"""
Created on Tue Oct 22 18:46:41 2019

@author: JVM
"""
import request, tempfile, os
#converter api help http://synbiodex.github.io/SBOL-Validator/?javascript#introduction

def DNA_to_GenBank(filename, partname):    
    newfile_url = "http://song.ece.utah.edu/examples/pages/acceptNewFile.php"
   
    temp = tempfile.NamedTemporaryFile(suffix=".dna")
    get_url = "http://song.ece.utah.edu/dnafiles/" + os.path.basename(temp.name)[:-4]
    partfile = request.get(filename).content

    temp.write(partfile)
    temp.flush()
    temp.seek(0)

    files = {'fileToUpload': temp}
    
    #upload file
    res = request.post(newfile_url, files=files,
                      headers = {"Accept":"text/plain"})
    #print(res)
    temp.close()

    
    #request genebank
    s = request.get(f"{get_url}.gb")
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
    
    resp = request.post("https://validator.sbolstandard.org/validate/", json=request)

   
    content = resp.json()
    return content["result"]
