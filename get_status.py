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


print(XNOW, YNOW)