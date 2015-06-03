from flask import Flask, request, abort
from bson import json_util

app = Flask(__name__)

app.config.from_envvar('DC_CONFIG_FILE')

import DeviceController.views
