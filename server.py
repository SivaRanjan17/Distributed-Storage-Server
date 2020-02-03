# -*- coding: utf-8 -*-
"""
Created on Sun Feb  2 08:29:00 2020

@author: 17pw33
"""
from flask import Flask, request, flash, redirect, send_file
#from flask_restful import Resource, Api
from pathlib import Path
from flask_jsonpify import jsonify
import json
import os
import uuid
import csv
from werkzeug.utils import secure_filename
import glob
from requests.models import Response
import sys
import shutil
from fsplit.filesplit import FileSplit

if (os.path.exists('uploads')):    
    shutil.rmtree("uploads")
os.mkdir("uploads")
#files = glob.glob('uploads/*')
#for f in files:
#    os.remove(f)

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])


class File(object):

    def __init__(self, file_name, path):
        self.file_name = file_name
        self.path = path
        self.size = os.path.getsize("uploads/" + file_name)
        self.id = uuid.uuid4()
        self.chunks = []
        
    def get(self):
        return self.id, self.file_name, self.path
        
    def __str__(self):
        print ("file name: ", self.file_name)
        print ("file path: ", self.path)
        print ("file size: ", self.size, "bytes")
        print ("file id: ", self.id)
        print ("file chunks: ", self.chunks)
        return ""

Files = []
"""
def write_to_csv(obj):
    with open('files.csv', mode='w') as file1:
        writer = csv.writer(file1, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow([obj.file_name, obj.path, obj.size, obj.id])
"""



def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

UPLOAD_FOLDER = 'C:/KLA/Cloud Object Storage/uploads'
with open('config.json') as f: #../Student Handout PSG _V2/Validator_Windows_V2
  data = json.load(f)

UPLOAD_FOLDER = str(os.path.abspath(data['storage_directory']).replace('\\', '/'))
size_slice = int(data['size_per_slice']) 
#print (data(size_per_slice'))
#"""
api = Flask(__name__)
api.secret_key = "secret key"
api.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
api.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

number_of_nodes = data['node_count']
path = UPLOAD_FOLDER
load = []
print (path)
for i in range(0, number_of_nodes):
    name = "node_" + str(i + 1)
    os.mkdir("uploads/" + name)
    load.append(0)

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])


#api = Api(api)

@api.route("/files/<arg>", methods=["GET"])
def download(arg):
    files = glob.glob('uploads/*.*')
    for f in files:
        os.remove(f)
    if (str(arg) == 'list'):
        result = []
        for obj in Files:
            odict = {}
            odict["file_name"] = obj.file_name
            odict["id"] = obj.id
            result.append(odict)
            
        response = jsonify(result)
        response.status_code = 200
        return response
           
        
    else:
        downfile = None
        for obj in Files:
            #print ("ID: ", obj.id, arg)
            if (str(obj.id) == str(arg)):
                downfile = obj
                #print (downfile)
        if (downfile):  
            print (downfile.chunks)
            file = open("uploads/" + downfile.file_name, "w")
            n = 1
            for path in downfile.chunks:
                if (n > len(downfile.chunks) / 2):
                    break
                temp_file = open(path, "r")
                temp_file = None
                try:
                    temp_file = open(path, "r")
                except IOError:
                    path1 = downfile[len(downfile.chunks) - (downfile.chunks.index(path) + 1)]
                    temp_file = open(path1, "r")
                
                data = temp_file.read()
                file.write(data)
                n += 1
                
            file.close()                
            path = "C:/KLA/Cloud Object Storage/uploads/"+ downfile.file_name
            #print (downfile)
            response = send_file(path, as_attachment=True)
            response.headers['content-type'] = "application/octet-stream"
            response.status_code = 200
            #os.remove("uploads/" + downfile.file_name)
            return response,200  # send_file(path, as_attachment=True), 200"""
        else:
            response = jsonify({'message' : "requested object " + str(arg) + " is not found"})
            response.status_code = 404
            response.headers['content-type'] = "text/plain"
            return response
    
@api.route("/files", methods=["PUT"])
def upload_file():
    files = glob.glob('uploads/*.*')
    for f in files:
        os.remove(f)
    
    if 'file' not in request.files:
            resp = jsonify({'message' : 'No file part in the request'})
            resp.status_code = 400
            return resp
    file = request.files['file']
    
    if file.filename == '':
        resp = jsonify({'message' : 'No file selected for uploading'})
        resp.status_code = 400
        return resp
    
    if file and allowed_file(file.filename):
        #print(os.path.getsize(file.filename))
        filename = secure_filename(file.filename)
        for obj in Files:
            if (obj.file_name == filename):
                return "file already exists", 409
    
        file.save(os.path.join(api.config['UPLOAD_FOLDER'], filename))
        fobj = File(filename, os.path.abspath(filename))
        #print(os.path.getsize('uploads/' + filename))
        file1 = open("uploads/" + filename, "r")
        file_size = int(os.path.getsize("uploads/" + filename))
        filecount = 1
        while (file_size > 0):
            data = file1.read(size_slice) # Replace with variable
            path = load.index(min(load)) + 1
            #print (path)
            temp_file = open("uploads/node_" + str(path) + "/"  + filename + '_' + str(filecount), "w")
            temp_file.write(data)
            temp_file.close()
            '''----------------------------------------------------'''
            path1 = number_of_nodes + 1 - path
            temp_file = open("uploads/node_" + str(path1) + "/"  + filename + '_' + str(filecount), "w")
            temp_file.write(data)
            temp_file.close()
            '''----------------------------------------------------'''
            fobj.chunks.append("uploads/node_" + str(path) + "/"  + filename + '_' + str(filecount))
            fobj.chunks.append("uploads/node_" + str(path1) + "/"  + filename + '_' + str(filecount))
            filecount += 1
            file_size -= size_slice
            load[path - 1] += 1
        file1.close()    
        #print (fobj)
        Files.append(fobj)
        os.remove("uploads/" + filename)
        #print(fobj)
        #response = jsonify({'message' : str(fobj.id)})
        #response.status_code = 200
        #response.headers['content-type'] = "text/plain" 
        return str(fobj.id), 200
    
    else:
        resp = jsonify({'message' : 'Allowed file types are txt, pdf, png, jpg, jpeg, gif'})
        resp.status_code = 401
        return resp

@api.route("/files/<arg>", methods=["DELETE"])    
def delete_file(arg):
    files = glob.glob('uploads/*.*')
    for f in files:
        os.remove(f)
    downfile = None
    print ("ARG: ", arg)
    for obj in Files: #i in range(0, len(Files)):
        print ("FileID: ", obj.id, len(Files))
        if (str(obj.id) == str(arg)):
            downfile = obj
            
    if (downfile): 
        print ("HELLO: ", downfile.file_name)
        file = open("uploads/" + downfile.file_name, "w")
        for path in downfile.chunks:
            temp_file = open(path, "r")
            data = temp_file.read()
            temp_file.close()
            os.remove(path)
            file.write(data)
        file.close()                
        path = "C:/KLA/Cloud Object Storage/uploads/"+ downfile.file_name
        #downfile = Files[i].file_name
        os.remove("uploads/" + downfile.file_name)
        Files.remove(downfile)#pop(i).id
        response = jsonify({'message' :"object " + str(downfile.id) + " deleted successfully"})
        response.status_code = 200
        response.headers['content-type'] = "text/plain" 
        return response

    else:
        
        response = jsonify({'message' : "Requested object " + str(arg) + " is not found"})
        response.status_code = 404
        response.headers['content-type'] = "text/plain" 
        return response         
        
    

if __name__ == "__main__":
    api.run(port = "5000")
#"""

