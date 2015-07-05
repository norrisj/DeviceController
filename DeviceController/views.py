from DeviceController import app, verify_user, verify_user_isadmin
from flask import Flask, request, abort, jsonify
from VideoRecord import VideoRecord
from mongoengine import *
import json
from jsonschema import validate, ValidationError

@app.route('/videos', methods=['GET'] )
@verify_user
def getmovements():
    ids = []
    for i in VideoRecord.objects:
        ids.append ( str(i.id) )

    return json.dumps( ids )

@app.route('/videos', methods=['POST'] )
@verify_user_isadmin
def postmovements():
    recordIn = request.get_json(force=True)

    try:
        validate(recordIn, VideoRecord.get_json_schema())
    except ValidationError:
        abort(400)

    post = VideoRecord.from_json( json.dumps(recordIn))
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
