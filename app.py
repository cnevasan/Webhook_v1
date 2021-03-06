# -*- coding:utf8 -*-
# !/usr/bin/env python
# Copyright 2017 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import print_function
from future.standard_library import install_aliases
install_aliases()

from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError

import json
import os

from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))

    res = processRequest(req)

    res = json.dumps(res, indent=4)
    # print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


def processRequest(req):
    if req.get("result").get("action") != "CheckCityDate":
        return {}

    #result = req.get("result")
    #parameters = result.get("parameters")
    city = req.get("result").get("parameters").get("geo-city")
    #if city is None:
    #    return 'Jasper'
    #else:
    #    return city
     
    ddate = GetDate(city)

    #if cdate is None:
    #    return {}
    speech = "We will be in your city:"+ city + " on " + ddate
    data = city+ddate
    return {
        "speech": speech,
        "displayText": speech,
        #"city": city,
        #"cdate": cdate,
         "data": data,
        # "contextOut": [],
        "source": "apiai-weather-webhook-sample"
           }

def GetDate(city):
    d = {'Jasper':'05-Feb-2018','Edmonton':'12-Feb-2018','Saskatoon':'08-Mar-2018','Thunder Bay':'26-Mar-2018'}
    cdate = d.get(city,'TBC')
    return cdate

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=False, port=port, host='0.0.0.0')
