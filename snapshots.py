import asyncio, sys, os
from onvif import ONVIFCamera
import time

IP = '192.168.1.118'
PORT = 80
USER = 'admin'
PASS = 'Nawgati!1806'

XMAX, XMIN, XNOW, YMAX, YMIN, YNOW = 1, -1, 0.5, 1, -1, 0.5

Move, Velocity, Zoom = 0.1, 2, 0

positionrequest = None
ptz = None
active = False
ptz_configuration_options = None
media_profile = None


def perform_move(ptz, request):
    global active
    if active:
        ptz.Stop({'ProfileToken': request.ProfileToken})
    active = True
    ptz.AbsoluteMove(request)


#Absolute move functions
def move_up(ptz, request, move):
    print(request.Position.PanTilt.x, request.Position.PanTilt.y)
    
    if YNOW + move >= 1.0:
        request.Position.PanTilt.y = YNOW + (1.0 - YNOW)
        print('Reached maximum limit')
    else:
        request.Position.PanTilt.y = YNOW + move
    
    print(request.Position.PanTilt.x, request.Position.PanTilt.y)
    
    perform_move(ptz, request)


def moving_up(step):
    move = step
    setup()
    get_status()
    move_up(ptz, positionrequest, move)
    
    
def move_down(ptz, request, move):
    print(request.Position.PanTilt.x, request.Position.PanTilt.y)
    if YNOW - move <= -1:
        request.Position.PanTilt.y = YNOW + (-1.0 + YNOW)
        print('Reached maximum limit')
    else:
        request.Position.PanTilt.y = YNOW - move
    
    print(request.Position.PanTilt.x, request.Position.PanTilt.y)
    
    perform_move(ptz, request)
    

def moving_down(step):
    move = step
    setup()
    get_status()
    move_down(ptz, positionrequest, move)
    

def move_left(ptz, request, move):
    print(request.Position.PanTilt.x, request.Position.PanTilt.y)
    if XNOW - move >= -0.99:
        request.Position.PanTilt.x = XNOW - move
    elif abs(XNOW + move) >= 0.0:
        request.Position.PanTilt.x = abs(XNOW) - move
    elif abs(XNOW) <= 0.01:
        request.Position.Pantilt.x = XNOW
    
    request.Position.PanTilt.y = YNOW
    print(request.Position.PanTilt.x, request.Position.PanTilt.y)
    perform_move(ptz, request)
    

def moving_left(step):
    move = step
    setup()
    get_status()
    move_left(ptz, positionrequest, move)
    

def move_right(ptz, request, move):
    print(request.Position.PanTilt.x, request.Position.PanTilt.y)
    if XNOW + move <= 1.0:
        request.Position.PanTilt.x = XNOW + move
    elif XNOW <= 1.0 and XNOW > 0.99:
        request.Position.PanTilt.x = -XNOW
    elif XNOW < 0:
        request.Position.PanTilt.x = XNOW + move
    elif XNOW <= 0.105556 and XNOW >- 0.11:
        request.Position.PanTilt.x = XNOW
    
    request.Position.PanTilt.y = YNOW
    print(request.Position.PanTilt.x, request.Position.PanTilt.y)
    perform_move(ptz, request)


def moving_right(step):
    move = step
    setup()
    get_status()
    move_right(ptz, positionrequest, move)


def zoom_in(ptz, request, move):
    print(request.Position.Zoom.x)
    
    if Zoom + Move >= 1.0:
        request.Position.Zoom = 1.0
        print("Maximum Zoom Limit Reached")
    else:
        request.Position.Zoom = Zoom + Move
        print("Zooming in ...")
    
    print(request.Position.Zoom)
    perform_move(ptz, request)
    

def zooming_in(step):
    move = step
    setup()
    get_status()
    zoom_in(ptz, positionrequest, move)
    

def zoom_out(ptz, request, move):
    print(request.Position.Zoom.x)
    
    if Zoom - Move <= 0.0:
        request.Position.Zoom = 0.0
        print("Minimum Zoom Limit Reached")
    else:
        request.Position.Zoom = Zoom - Move
        print("Zooming Out ...")
    
    perform_move(ptz, request)
    print(request.Position.Zoom)
    

def zooming_out(step):
    move = step
    setup()
    get_status()
    zoom_out(ptz, positionrequest, move)


# Checking if camera is idle
def check_camera_idle():
	myCam = ONVIFCamera(IP, PORT, USER, PASS)
	media_service = myCam.create_media_service()
	profile = media_service.GetProfiles()[0]

	ptz_service = myCam.create_ptz_service()

	# checking if camera supports PTZ
	if not ptz_service:
		print('PTZ not supported by camera')
	else:
		print('PTZ supported by camera')

	status = ptz_service.GetStatus({'ProfileToken': profile.token})

	# checking if PTZ functionality is active or not
	if status.Position and status.Position.PanTilt:
		print("PTZ functionality is active")
	else:
		print("PTZ functionality is inactive")

	# checking if PTZ camera is in moving state or not
	if status.Position and status.Position.PanTilt and (status.MoveStatus['PanTilt'] == 'IDLE' or status.MoveStatus['Zoom'] == 'IDLE'):
		print('PTZ is not in moving state')
	else:
		print('PTZ is in moving state')


XMAX, XMIN, XNOW, YMAX, YMIN, YNOW = 1, -1, 0, 1, -1, 0
positionrequest = None
ptz = None
ptz_configuration_options = None
media_profile = None
IP = '192.168.1.118'
PORT = 80
USER = 'admin'
PASS = 'Nawgati!1806'


def setup():
    myCam = ONVIFCamera(IP, PORT, USER, PASS)
    
    media = myCam.create_media_service()

    global ptz, ptz_configuration_options, media_profile
    ptz = myCam.create_ptz_service()
    media_profile = media.GetProfiles()[0]
    
    request = ptz.create_type('GetConfigurationOptions')
    request.ConfigurationToken = media_profile.PTZConfiguration.token
    ptz_configuration_options = ptz.GetConfigurationOptions(request)

    request_configuration = ptz.create_type('GetConfiguration')
    request_configuration.PTZConfigurationToken = media_profile.PTZConfiguration.token
    ptz_configuration = ptz.GetConfiguration(request_configuration)

    request_setconfiguration = ptz.create_type('SetConfiguration')
    request_setconfiguration.PTZConfiguration = ptz_configuration
    
    global positionrequest
    
    positionrequest = ptz.create_type('AbsoluteMove')
    positionrequest.ProfileToken = media_profile.token
    
    if positionrequest.Position is None:
        positionrequest.Position = ptz.GetStatus({'ProfileToken': media_profile.token}).Position
        positionrequest.Position.PanTilt.space = ptz_configuration_options.Spaces.AbsolutePanTiltPositionSpace[0].URI
        positionrequest.Position.Zoom.space = ptz_configuration_options.Spaces.AbsoluteZoomPositionSpace[0].URI
        
    if positionrequest.Speed is None:
        positionrequest.Speed = ptz.GetStatus({'ProfileToken': media_profile.token}).Position
        positionrequest.Speed.PanTilt.space = ptz_configuration_options.Spaces.PanTiltSpeedSpace[0].URI


def get_status():
    global XMAX, XMIN, XNOW, YMAX, YMIN, YNOW, Velocity, Zoom
    
    XMAX = ptz_configuration_options.Spaces.AbsolutePanTiltPositionSpace[0].XRange.Max
    XMIN = ptz_configuration_options.Spaces.AbsolutePanTiltPositionSpace[0].XRange.Min
    YMAX = ptz_configuration_options.Spaces.AbsolutePanTiltPositionSpace[0].YRange.Max
    YMIN = ptz_configuration_options.Spaces.AbsolutePanTiltPositionSpace[0].YRange.Min
    
    XNOW = ptz.GetStatus({'ProfileToken': media_profile.token}).Position.PanTilt.x
    YNOW = ptz.GetStatus({'ProfileToken': media_profile.token}).Position.PanTilt.y
    
    Velocity = ptz_configuration_options.Spaces.PanTiltSpeedSpace[0].XRange.Max
    Zoom = ptz.GetStatus({'ProfileToken': media_profile.token}).Position.Zoom.x


def leftmost_left_1():
    zooming_out(1)
    time.sleep(5)
    !curl -L --digest -u admin:Nawgati\!1806 -D - "http://192.168.1.118/ISAPI/Streaming/channels/1/picture" -o 118.jpg
    time.sleep(5)
    moving_right(0.24)
    time.sleep(5)
    moving_up(0.05)
    time.sleep(5)
    zooming_in(0.1)
    zooming_in(0.01)
    get_status()
    print(XNOW, YNOW, Zoom)


def left_1_right_1():
    !curl -L --digest -u admin:Nawgati\!1806 -D - "http://192.168.1.118/ISAPI/Streaming/channels/1/picture" -o 118.jpg
    time.sleep(5)
    moving_right(0.15)
    time.sleep(5)
    moving_up(0.1)
    time.sleep(5)
    zooming_in(0.1)
    get_status()
    print(XNOW, YNOW, Zoom)


def right_1_rightmost():
    !curl -L --digest -u admin:Nawgati\!1806 -D - "http://192.168.1.118/ISAPI/Streaming/channels/1/picture" -o 118.jpg
    time.sleep(5)
    moving_right(0.02)
    time.sleep(5)
    moving_up(0.05)
    time.sleep(5)
    zooming_in(0.1)
    time.sleep(2)
    zooming_in(0.1)
    get_status()
    print(XNOW, YNOW, Zoom)


def rightmost_leftmost():
    !curl -L --digest -u admin:Nawgati\!1806 -D - "http://192.168.1.118/ISAPI/Streaming/channels/1/picture" -o 118.jpg
    time.sleep(5)
    zooming_out(0.5)
    time.sleep(5)
    zooming_out(0.5)
    time.sleep(5)
    moving_left(0.4)
    time.sleep(5)
    moving_down(0.2)
    get_status()
    print(XNOW, YNOW, Zoom)


def snapshots():
    leftmost_left_1()
    left_1_right_1()
    right_1_rightmost()
    rightmost_leftmost()


setup()
snapshots()