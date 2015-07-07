from DeviceController import app, verify_user, verify_user_isadmin
from flask import Flask, request, abort, jsonify
from mongoengine import *
from SensorRecord import SensorRecord
import json
from jsonschema import validate, ValidationError

@app.route('/sensors', methods=['GET'] )
@verify_user_isadmin
def getsensors():
    ids = []
    for i in SensorRecord.objects:
        ids.append ( str(i.sensorid) )
    return json.dumps( ids )
