import json
import os
from flask_jsonpify import jsonify
with open('config.json') as f: #../Student Handout PSG _V2/Validator_Windows_V2
    data = json.load(f)
    
file = open()    
    
print (data)
#str1 = "REQ"
#list1 = []
#list1.append(str1)
#response = jsonify(list1)
#print (response)

"""
class FileServer(Resource):
    
    def get(self, arg):
        if (arg == 'list'):          
            file_dict = []
            entries = Path('Uploads/')
            #result = {'data': [dict(zip(tuple("file_name"), entry.name)) for entry in entries.iterdir()]}
            for entry in entries.iterdir():
                print(entry.name)
                file_dict.append({"file_name" : entry.name})
                            
            return jsonify(file_dict)
        
        else:
            downfile = None
            for obj in Files:
                if (obj.id == arg):
                    downfile = obj.path
            #path = "C:/KLA/Cloud Object Storage/uploads/test_file_1.txt"
            return send_file(downfile, as_attachment=True)
            #uploads = os.path.join(current_app.root_path, app.config['UPLOAD_FOLDER'])
            #return send_from_directory(directory=uploads, filename=filename)
        
    def put(self):
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
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            fobj = File(filename, os.path.abspath(filename))
            Files.append(fobj)
            print(fobj)
            resp = jsonify({'id' : fobj.id})
            resp.status_code = 201
            return resp
        else:
            resp = jsonify({'message' : 'Allowed file types are txt, pdf, png, jpg, jpeg, gif'})
            resp.status_code = 400
            return resp

    def delete(self, arg):
        return{
                "Status" : "NOT OK"
                }        
#"""       
#with open('config.json') as f: #../Student Handout PSG _V2/Validator_Windows_V2
#  data = json.load(f)

#print(data)    



#api.add_resource(FileServer, "/files/<arg>")
#api.add_resource(FileServer, "/files")
#uploads = os.path.join(current_app.root_path, app.config['UPLOAD_FOLDER'])
#return send_from_directory(directory=uploads, filename=filename)
"""Endpoint to list files on the server
    files = []
    for filename in os.listdir(UPLOAD_DIRECTORY):
        path = os.path.join(UPLOAD_DIRECTORY, filename)
        if os.path.isfile(path):
            files.append(filename)
    return jsonify(files) 
"""
