#!/usr/bin/python

from datetime import datetime
import json
import urllib
import urllib2

from bottle import route, run, debug, template, request, redirect
import pytz
from settings import *


@route("/")
def chat():
    # get the request time in UTC and localize it
    request_time = datetime.utcnow().replace(tzinfo = pytz.utc)
    user_tz = pytz.timezone(TIME_ZONE)
    loc_dt = request_time.astimezone(user_tz)

    # set active hours for chat
    chat_open = loc_dt.replace(hour=OPEN_HR, 
                               minute=OPEN_MIN,
                               second=0,
                               microsecond=0)
    
    chat_close = loc_dt.replace(hour=CLOSE_HR,
                                minute=CLOSE_MIN,
                                second=0,
                                microsecond=0)

    if loc_dt.isoweekday() in range(1,5) and \
       loc_dt >= chat_open and loc_dt <= chat_close:
        room_fields = create_room(loc_dt)
        room_name = room_fields['name']
        guest_url = room_fields['guest_access_url']
        message_room(room_name, guest_url)
        redirect(guest_url)
    else:
        return template('chat_offline')
    
def create_room(loc_dt):
    room_time = loc_dt.strftime("%I:%M %p %s")
    base_url = 'https://api.hipchat.com/v1/rooms/create'
    params = {
        'name': "Live Chat - " + room_time,
        'owner_user_id': OWNER_USER_ID,
        'privacy': 'public',
        'topic': TOPIC,
        'guest_access': 1,
        'format': 'json',
        'auth_token': ADMIN_TOKEN
        }
    params = urllib.urlencode(params)
    request = urllib2.Request(base_url, params)

    try:
        response = urllib2.urlopen(request)
        response_fields = json.loads(response.read())['room']
        return response_fields
    except urllib2.HTTPError, e:
        print e

def message_room(name, url):
    f_url = "<a href=\"%s\">%s</a>" % (url, url)
    msg = ("Somone needs help in <strong>%s</strong>. Join the "
           "conversation via the Lobby or visit as a guest @ %s"
           % (name, f_url))

    base_url = 'https://api.hipchat.com/v1/rooms/message'
    params = {
        'room_id': NOTIFY_ROOM_ID,
        'from': 'Web chat',
        'message': msg,
        'notify': 1,
        'color': 'red',
        'format': 'json',
        'auth_token': ADMIN_TOKEN
    }

    params = urllib.urlencode(params)
    request = urllib2.Request(base_url, params)

    try:
        response = urllib2.urlopen(request)
        response_fields = json.loads(response.read())
        return
    except urllib2.HTTPError, e:
        print e


if DEBUG_MODE: debug(True)

run(host=SERVER_HOST, port=SERVER_PORT, reloader=True)
