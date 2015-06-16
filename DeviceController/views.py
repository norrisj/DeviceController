from DeviceController import app
from flask import Flask, request, abort, jsonify
from VideoRecord import VideoRecord
from mongoengine import *
import json
from jsonschema import validate, ValidationError

@app.route('/videos', methods=['GET', 'POST'] )
def movements():
    if request.method == 'GET':
        ids = []
        for i in VideoRecord.objects:
            ids.append ( str(i.id) )

        return json.dumps( ids )
    else:
        recordIn = request.get_json(force=True)

        try:
            validate( recordIn, VideoRecord.get_json_schema() )
        except ValidationError:
            abort(400)

        post = VideoRecord.from_json( json.dumps(recordIn))
#        post.from_json( json.dumps(recordIn) )
        post.save()
        return str(post.id)

@app.route('/videos/<_id>', methods=['GET', 'DELETE'] )
def movement(_id):
    err = 400
    try:
        doc = VideoRecord.objects.get(id = _id)
        if request.method == 'DELETE':
            doc.delete()
        return doc.to_json()
        
    except DoesNotExist:
        err = 404
    except:
        pass
    abort ( err )
