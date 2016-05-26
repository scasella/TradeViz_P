#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from os import environ as env
from sys import argv

import bottle
from bottle import default_app, request, route, response, get
import json

_allow_origin = '*'
_allow_methods = 'GET'
_allow_headers = 'Authorization, Origin, Accept, Content-Type, X-Requested-With'

@hook('after_request')
def enable_cors():
    '''Add headers to enable CORS'''

    response.headers['Access-Control-Allow-Origin'] = _allow_origin
    response.headers['Access-Control-Allow-Methods'] = _allow_methods
    response.headers['Access-Control-Allow-Headers'] = _allow_headers

@get('/')
def main():
    try:
        try:
            data = request.json()
        except:
            raise ValueError

        if data is None:
            raise ValueError

    except ValueError:
        response.status = 400
        return

    except KeyError:
        response.status = 409
        return

    response.headers['Content-Type'] = 'application/json'
    return json.dumps({'test': data})

bottle.run(host='0.0.0.0', port=argv[1])
