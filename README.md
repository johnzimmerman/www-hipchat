# www-hipchat
www-hipchat is a simple script that allows existing [HipChat](https://www.hipchat.com/) customers to add live chat to their website. When a link is clicked during business hours a room is created, the staff is notified and the user is redirected to the newly created room. 

## Requirements
After downloading the source, run:

	$>pip install -r requirements.txt

## Configuration
Rename ```settings.py.example``` to ```settings.py```

```./views/chat_offline.tpl``` is the template the user is forwarded to when chat is offline. Edit it however you like.

### Available settings

#### ADMIN_TOKEN
Your HipChat administrator API token

#### OWNER_USER_ID
A room owner is assigned to a room when it’s created. In order to send messages to a particualr room, the owner ID is needed. See [this page](https://www.hipchat.com/docs/api/method/rooms/list) for help.

#### NOTIFY_ROOM_ID
The ID of the room being notified of newly created chat requests. Get a list of your room IDs [here](https://www.hipchat.com/rooms/ids).

#### TOPIC
The default topic of newly created rooms.

#### TIME_ZONE 
The time zone is used to convert UTC time to the user’s local time.

#### OPEN_HR
The hour (24-hour clock) at which chat becomes active.

#### OPEN_MIN
The minute at which chat becomes active.

#### CLOSE_HR
The hour (24-hour clock) at which chat closes.

#### CLOSE_MIN
The minute at which chat becomes active.

#### SERVER_HOST
Server host

#### SERVER_PORT
Server port

#### DEBUG_MODE
Enable debug mode. Set to ```False``` in a production environment.

## Deployment
www-hipchat uses the bottle.py micro web-framework. Please see bottle’s [deployment documentation](http://bottlepy.org/docs/stable/deployment.html) for deployment instructions.
