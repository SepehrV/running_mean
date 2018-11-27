# -*- coding: utf-8 -*-
"""
    running average data structure interface
    ~~~~~~

"""
import os
import time
import json
import uuid
from rq import Connection, Queue
import redis
import requests
from flask import Flask, request, url_for, abort, \
     render_template, send_from_directory, Response, redirect

from store import store_number


app = Flask(__name__, template_folder='templates')

app.config.update(dict(
    DEBUG=True,
    ENVIRONMENT= "development",
))

conn = redis.from_url('redis://localhost:6379')
q = Queue(connection=conn)

@app.route('/trait')
def trait():
    return render_template('trait.html')

@app.route('/insert',methods=["GET", "POST"])
def insert():
    data = dict(request.get_json())['data']
    if "value" not in data:
        return json.dumps({'success':False, 'err':'value is missing'},
                          200,
                          {'ContentType':'application/json'})
    try:
        data['value'] = int(data['value'])
    except:
        return json.dumps({'success':False, 'err':'value must be an int'},
                          200,
                          {'ContentType':'application/json'})


    data.update({'timestamp':time.time()})
    data['value'] = str(data['value'])+'_'+str(uuid.uuid4())[0:8]
    q.enqueue(store_number, data)
    return json.dumps({'success':True},
                      200,
                      {'ContentType':'application/json'})

@app.route('/demo',methods=["GET", "POST"])
def demo():
    return render_template('demo.html')


@app.route('/getMean',methods=["GET", "POST"])
def getMean():
    data = dict(request.get_json())['data']
    user=data['user']
    N = int(data['N'])
    if N==0:
        return None
    n = min(conn.zcard(user), N)
    stored_vals =  conn.zrange(user, -N, -1)
    numbers = list(map(int,[str(x).split('_')[0][2:] for x in stored_vals]))
    mean = sum(numbers)/n
    return json.dumps({'success':True, 'mean':mean, 'numbers':str(numbers)},
                      200,
                      {'ContentType':'application/json'})


if __name__=='__main__':
    app.run(host='0.0.0.0', port=8888)


