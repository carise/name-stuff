import bottle
from bottle import route, redirect, post, run, request, hook, template, static_file
import pymongo
from pymongo import MongoClient

DEBUG=False
SERVER_PORT=80 if not DEBUG else 8080

bottle.debug(DEBUG)


bottle.run(host='0.0.0.0', port=SERVER_PORT)
