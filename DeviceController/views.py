from DeviceController import app
from flask import Flask, request, abort
from VideoRecord import VideoRecord
from mongoengine import *
import json

@app.route("/")
def index():
    return "Hello world"

@app.route("/movements", methods=['GET', 'POST'] )
def movements():
    if request.method == 'GET':
        ids = []
        for i in VideoRecord.objects:
            ids.append ( str(i.id) )

        return json.dumps( ids )
    else:
        post = VideoRecord(testing="123").save()
        return str(post.id)

@app.route("/movements/<id>", methods=['GET'] )
def movement(_id):
    err = 400
    try:
        doc = VideoRecord.objects (id = _id)
        if ( doc is None ):
            err = 404
        else:
            return json.dumps ( doc, default=json_util.default ) 
    except:
        pass
    abort ( err )
