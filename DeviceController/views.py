from DeviceController import app
from flask import Flask, request, abort, jsonify
from VideoRecord import VideoRecord
from mongoengine import *
import json

@app.route("/")
def index():
    return "Hello world"

@app.route('/movements', methods=['GET', 'POST'] )
def movements():
    if request.method == 'GET':
        ids = []
        for i in VideoRecord.objects:
            ids.append ( str(i.id) )

        return json.dumps( ids )
    else:
        recordIn = request.get_json(force=True)

        post = VideoRecord.from_json( json.dumps(recordIn))
#        post.from_json( json.dumps(recordIn) )
        post.save()
        return post.testing

@app.route('/movements/<_id>', methods=['GET'] )
def movement(_id):
    err = 400
    try:
        doc = VideoRecord.objects.get(id = _id)
        return doc.to_json()
    except DoesNotExist:
        err = 404
    except:
        pass
    abort ( err )
